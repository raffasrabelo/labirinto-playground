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
        if (document.activeElement !== $("#q_values")) $("#q_values").value = p.q_values;
        renderQValuesWarning(p.q_values, state.q_fit);
        const legend = HEAT_LEGEND[p.q_values] || HEAT_LEGEND.off;
        if ($("#heat-legend").textContent !== legend) $("#heat-legend").textContent = legend;
        renderInspector(state.inspect);

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

    // ----------------------------- valores e inspetor da tabela Q --
    const dec1 = new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
    const Q_WARN = {
        one: "Nesta grade os números não cabem nas células: as cores continuam mostrando o valor escolhido. Passe o mouse para ver os números no inspetor.",
        all: "Os 4 valores só cabem em grades pequenas (11 × 11 ou 13 × 13). Use V(s) ou uma única ação, ou o inspetor ao lado.",
    };
    // texto da legenda do mapa de calor para cada modo de visualização
    const HEAT_LEGEND = {
        off: "Valor aprendido V(s) (baixo → alto)",
        max: "V(s) = maior Q (baixo → alto)",
        all: "V(s) = maior Q (baixo → alto)",
        up: "Q(s, ↑) (baixo → alto)",
        right: "Q(s, →) (baixo → alto)",
        down: "Q(s, ↓) (baixo → alto)",
        left: "Q(s, ←) (baixo → alto)",
        visits: "Visitas (poucas → muitas)",
    };

    function renderQValuesWarning(mode, fit) {
        const warn = $("#q-values-warn");
        const key = mode === "all" ? "all" : "max";
        const show = mode !== "off" && Boolean(fit) && !fit[key];
        const text = mode === "all" ? Q_WARN.all : Q_WARN.one;
        warn.hidden = !show;
        if (show && warn.textContent !== text) warn.textContent = text;
    }

    function renderInspector(info) {
        const cells = $$("#insp-cross .q");
        const note = $("#insp-note");
        let noteText = "Passe o mouse sobre uma célula do labirinto.";
        $("#insp-visits").textContent = info ? fmt.format(info.visits || 0) : "–";
        if (!info) {
            $("#insp-cell").textContent = "–";
            cells.forEach((el) => { el.classList.remove("best"); el.lastElementChild.textContent = "–"; });
        } else {
            const where = "coluna " + info.cell[0] + ", linha " + info.cell[1];
            $("#insp-cell").textContent = info.source === "agent" ? where + " · agente" : where;
            cells.forEach((el) => {
                const a = Number(el.dataset.a);
                el.classList.toggle("best", info.best === a);
                el.lastElementChild.textContent = info.q ? dec1.format(info.q[a]) : "–";
            });
            if (info.wall) noteText = "Parede: o agente nunca está aqui, então não há valores.";
            else if (info.goal) noteText = "Objetivo: o episódio termina ao chegar, então não há valores.";
            else if (!info.q) noteText = "O agente ainda não passou por esta célula: todos os valores valem 0.";
            else if (info.source === "agent") noteText = "Mostrando a célula do agente. Passe o mouse sobre outra célula para inspecioná-la.";
            else noteText = "Q(s, a): quanto o agente espera ganhar daqui até o fim indo nessa direção. Sublinhado: a melhor ação.";
        }
        if (note.textContent !== noteText) note.textContent = noteText;
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

    $("#q_values").addEventListener("change", (e) => {
        send({ type: "set", name: "q_values", value: e.target.value });
    });

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
    const isTyping = (t) => t instanceof Element && t.matches("input[type=number], input[type=text], select");
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
        send({ type: "resize", w: Math.round(rect.width * dpr), h: Math.round(rect.height * dpr), dpr: dpr });
    }
    new ResizeObserver(reportSize).observe(wrap);
    // ao sair do labirinto, o inspetor volta a mostrar a célula do agente
    $("#canvas").addEventListener("mouseleave", () => send({ type: "hover_clear" }));
    window.addEventListener("resize", reportSize);
    reportSize();

    // --------------------------------- modo aplicativo nunca rola a página --
    // No modo aplicativo só as colunas rolam. Se o navegador rolar a página
    // (por exemplo, para mostrar um elemento focado), ela volta ao topo.
    const appMode = window.matchMedia("(min-width: 1181px) and (min-height: 640px)");
    document.addEventListener("scroll", () => {
        if (appMode.matches && (window.scrollY || document.body.scrollTop)) {
            window.scrollTo(0, 0);
            document.body.scrollTop = 0;
        }
    }, { passive: true });
})();
