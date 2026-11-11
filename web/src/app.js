// =============================================================================
// Labirinto Playground · interface (HTML) <-> Python (pygbag)
//
// A página NÃO conhece os algoritmos: ela só envia comandos e mostra o estado.
//   send({ type: "set", name: "size", value: 31 })    -> fila lida pelo Python
//   labirinto.push(json)                                <- Python a cada mudança
// O formato das mensagens está documentado em docs/02-arquitetura.md.
// =============================================================================
(function () {
    "use strict";

    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => Array.from(document.querySelectorAll(sel));
    const fmt = new Intl.NumberFormat("pt-BR");

    const STATUS_TEXT = {
        idle: "Pronto para executar",
        running: "Executando",
        paused: "Pausado",
        found: "Caminho encontrado",
        no_path: "Não existe caminho",
    };

    // ---------------------------------------------------------- ponte --
    let queue = [];
    let ready = false;

    function send(cmd) {
        if (cmd.type === "resize") {
            queue = queue.filter((c) => c.type !== "resize");  // só o último importa
        }
        queue.push(cmd);
    }

    window.labirinto = {
        // chamado pelo Python a cada quadro
        pull() {
            if (!queue.length) return "";
            const data = JSON.stringify(queue);
            queue = [];
            return data;
        },
        // chamado pelo Python quando o estado muda
        push(json) {
            render(JSON.parse(json));
            if (!ready) {
                ready = true;
                document.body.classList.remove("is-loading");
                $("#canvas").focus();
            }
        },
        loading(text) {
            $("#loader-title").textContent = text;
        },
    };

    // ------------------------------------------------ velocidade (log) --
    // slider 0..100 -> 1..100.000 passos/s em escala logarítmica (o treino do
    // Q-Learning tem dezenas de milhares de passos)
    const speedFromSlider = (v) => Math.max(1, Math.round(Math.pow(10, (v / 100) * 5)));
    const sliderFromSpeed = (s) => Math.round((Math.log10(Math.max(1, s)) / 5) * 100);
    const speedLabel = (s) => `${fmt.format(s)} ${s === 1 ? "passo" : "passos"}/s`;

    // -------------------------------------------------------- render --
    const dec = (v) => fmt.format(Number(v));
    const outputs = {
        size: (v) => `${v} × ${v}`,
        openness: (v) => `${v}%`,
        mud: (v) => `${v}%`,
        alpha: dec,
        gamma: dec,
        epsilon: dec,
        decay: dec,
        episodes: (v) => fmt.format(Number(v)),
        goal_reward: (v) => `+${v}`,
        wall_penalty: (v) => (Number(v) === 0 ? "0" : `−${v}`),
    };
    const RANGE_PARAMS = Object.keys(outputs);
    const QL_DEFAULTS = { alpha: 0.5, gamma: 0.995, epsilon: 0.3, decay: 0.99, episodes: 200, goal_reward: 100, wall_penalty: 10 };

    function setText(sel, value) {
        const el = $(sel);
        const text = value === null || value === undefined ? "–" : fmt.format(value);
        if (el.textContent !== text) el.textContent = text;
    }

    function setChecked(groupSel, value) {
        $$(`${groupSel} button`).forEach((b) => {
            b.setAttribute("aria-checked", String(b.dataset.value === value));
        });
    }

    function render(state) {
        const p = state.params;
        document.body.dataset.algorithm = p.algorithm;
        document.body.dataset.mode = state.mode;

        setChecked("#algorithm", p.algorithm);
        setChecked("#brush", p.brush);

        for (const name of RANGE_PARAMS) {
            const input = $(`#${name}`);
            if (document.activeElement !== input) input.value = p[name];
            $(`#${name}-out`).textContent = outputs[name](p[name]);
        }
        if (document.activeElement !== $("#seed")) $("#seed").value = p.seed;
        if (document.activeElement !== $("#speed")) $("#speed").value = sliderFromSpeed(p.speed);
        $("#speed-out").textContent = speedLabel(p.speed);
        $("#show_numbers").checked = p.show_numbers;
        $("#show_policy").checked = p.show_policy;

        const m = state.metrics;
        setText("#m-steps", m.steps);
        setText("#m-visited", m.visited);
        setText("#m-frontier", m.frontier);
        setText("#m-depth", m.depth);
        setText("#m-maxdepth", m.max_depth);
        setText("#m-moves", m.moves);
        setText("#m-cost", m.cost);
        setText("#m-episode", m.episode);
        setText("#m-episodes", m.episodes);
        setText("#m-epsilon", m.epsilon);
        setText("#m-last-reward", m.last_reward);
        setText("#m-reached", m.reached);
        if (p.algorithm === "qlearning") drawChart(state.rewards);

        const pill = $("#status-pill");
        pill.dataset.status = state.status;
        const ql = p.algorithm === "qlearning";
        const statusText = ql && state.status === "found" ? "Caminho aprendido"
            : ql && state.status === "no_path" ? "O agente não aprendeu o caminho"
            : ql && state.status === "running" ? "Treinando"
            : STATUS_TEXT[state.status] || state.status;
        $("#status-text").textContent = statusText;

        $("#btn-play").setAttribute("aria-label", state.mode === "running" ? "Pausar" : "Executar");
        $("#btn-step").disabled = state.status === "found" || state.status === "no_path";
        if ($("#description").textContent !== state.description) {
            $("#description").textContent = state.description;
        }
    }

    // ---------------------------------- gráfico de recompensa (Q-Learning) --
    function drawChart(values) {
        const svg = $("#reward-chart");
        const key = `${values.length}:${values[values.length - 1]}:${values[0]}`;
        if (svg.dataset.key === key) return;
        svg.dataset.key = key;
        const W = 260, H = 120, L = 34, R = 6, T = 8, B = 16;
        if (!values.length) {
            svg.innerHTML = `<text x="${W / 2}" y="${H / 2}" text-anchor="middle">Execute para acompanhar o treino</text>`;
            return;
        }
        const min = Math.min(0, ...values), max = Math.max(0, ...values);
        const span = max - min || 1;
        const x = (i) => L + (values.length === 1 ? 0 : (i * (W - L - R)) / (values.length - 1));
        const y = (v) => T + ((max - v) * (H - T - B)) / span;
        const line = (arr) => arr.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ");
        // média móvel para mostrar a tendência por trás do ruído da exploração
        const k = Math.max(1, Math.round(values.length / 15));
        const avg = values.map((_, i) => {
            const part = values.slice(Math.max(0, i - k + 1), i + 1);
            return part.reduce((a, b) => a + b, 0) / part.length;
        });
        svg.innerHTML =
            `<line class="zero" x1="${L}" x2="${W - R}" y1="${y(0)}" y2="${y(0)}"/>` +
            `<line class="axis" x1="${L}" x2="${L}" y1="${T}" y2="${H - B}"/>` +
            `<text x="${L - 4}" y="${T + 7}" text-anchor="end">${fmt.format(Math.round(max))}</text>` +
            `<text x="${L - 4}" y="${H - B}" text-anchor="end">${fmt.format(Math.round(min))}</text>` +
            `<text x="${W - R}" y="${H - 3}" text-anchor="end">episódios →</text>` +
            `<polyline class="raw" points="${line(values)}"/>` +
            `<polyline class="avg" points="${line(avg)}"/>`;
    }

    // ------------------------------------------------------- eventos --
    $("#btn-play").addEventListener("click", () => send({ type: "play" }));
    $("#btn-step").addEventListener("click", () => send({ type: "step" }));
    $("#btn-reset").addEventListener("click", () => send({ type: "reset" }));
    $("#btn-new").addEventListener("click", () => send({ type: "new_maze" }));
    $("#btn-clear").addEventListener("click", () => send({ type: "clear" }));

    for (const group of ["algorithm", "brush"]) {
        $$(`#${group} button`).forEach((b) => {
            b.addEventListener("click", () => {
                send({ type: "set", name: group, value: b.dataset.value });
                setChecked(`#${group}`, b.dataset.value);  // resposta imediata
            });
        });
    }

    $$("input[type=range][data-param]").forEach((input) => {
        input.addEventListener("input", () => {
            const name = input.dataset.param;
            $(`#${name}-out`).textContent = outputs[name](input.value);
            send({ type: "set", name, value: Number(input.value) });
        });
    });

    $("#seed").addEventListener("change", (e) => {
        send({ type: "set", name: "seed", value: Number(e.target.value) });
    });

    $("#speed").addEventListener("input", (e) => {
        const speed = speedFromSlider(Number(e.target.value));
        $("#speed-out").textContent = speedLabel(speed);
        send({ type: "set", name: "speed", value: speed });
    });

    for (const name of ["show_numbers", "show_policy"]) {
        $(`#${name}`).addEventListener("change", (e) => {
            send({ type: "set", name, value: e.target.checked });
        });
    }

    $("#btn-ql-defaults").addEventListener("click", () => {
        for (const [name, value] of Object.entries(QL_DEFAULTS)) {
            send({ type: "set", name, value });
        }
    });

    // atalhos de teclado (ignorados enquanto se digita em um campo)
    const KEYS = { " ": "play", n: "step", N: "step", r: "reset", R: "reset", g: "new_maze", G: "new_maze" };
    const isTyping = (t) => t instanceof Element && t.matches("input[type=number], input[type=text]");
    document.addEventListener("keydown", (e) => {
        if (isTyping(e.target) || e.ctrlKey || e.metaKey || e.altKey || !(e.key in KEYS)) return;
        e.preventDefault();
        if (!e.repeat) send({ type: KEYS[e.key] });
    }, true);
    // evita que Espaço também "clique" no botão que estiver com foco
    document.addEventListener("keyup", (e) => {
        if (e.key === " " && !isTyping(e.target)) e.preventDefault();
    }, true);

    // ------------------------------------- tamanho real do labirinto --
    // O Python desenha na resolução física da tela (CSS x devicePixelRatio),
    // por isso o labirinto fica nítido em qualquer tamanho de janela.
    const wrap = $("#board-wrap");
    function reportSize() {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const rect = wrap.getBoundingClientRect();
        send({ type: "resize", w: Math.round(rect.width * dpr), h: Math.round(rect.height * dpr) });
    }
    new ResizeObserver(reportSize).observe(wrap);
    window.addEventListener("resize", reportSize);
    reportSize();
})();
