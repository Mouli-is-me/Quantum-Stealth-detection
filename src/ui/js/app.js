/* ==========================================================================
   Tactical HUD JavaScript - Quantum Sensor Fusion Dashboard (Streamlined)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // --------------------------------------------------
    // Configuration & State
    // --------------------------------------------------
    const state = {
        ping: 12,
        sensorStatus: {
            Radar: "ONLINE",
            Infrared: "ONLINE",
            Thermal: "ONLINE",
            Acoustic: "ONLINE"
        },
        sensorValues: {
            Radar: 82,
            Infrared: 68,
            Thermal: 76,
            Acoustic: 45
        },
        selection: {
            Radar: 1,
            Infrared: 0,
            Thermal: 1,
            Acoustic: 1
        },
        threatConfidence: 92,
        threatLevel: "CRITICAL", // LOW, MEDIUM, HIGH, CRITICAL
        recommendedAction: "INTERCEPT", // MONITOR, TRACK, INTERCEPT, IGNORE
        environment: {
            weather: "FOGGY",
            visibility: 1.2,
            noise: 72,
            wind: 14,
            temp: 18,
            stealth: 0.82
        },
        systemMetrics: {
            cpu: 34,
            mem: 52,
            qpu: 78,
            inferenceTime: 1.24,
            latency: 4.8
        },
        qubo: {
            energy: -2.845,
            iteration: 1024
        },
        confidenceHistory: [65, 70, 72, 68, 75, 80, 85, 88, 90, 92]
    };

    // Radar Map specific state
    const radarState = {
        angle: 0,
        targets: []
    };

    // --------------------------------------------------
    // Utilities & Clock
    // --------------------------------------------------
    function formatTime(date) {
        const h = String(date.getHours()).padStart(2, '0');
        const m = String(date.getMinutes()).padStart(2, '0');
        const s = String(date.getSeconds()).padStart(2, '0');
        return `${h}:${m}:${s}`;
    }

    function updateClock() {
        const timeElement = document.getElementById("hud-timestamp");
        if (timeElement) {
            timeElement.textContent = formatTime(new Date());
        }
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Fluctuating network latency
    setInterval(() => {
        state.ping = Math.max(8, Math.min(30, state.ping + Math.floor(Math.random() * 5) - 2));
        const pingElement = document.getElementById("ping-val");
        if (pingElement) {
            pingElement.textContent = `${state.ping}ms`;
        }
    }, 4000);

    // --------------------------------------------------
    // Tab Controller
    // --------------------------------------------------
    const tabRadarBtn = document.getElementById("btn-tab-radar");
    const tabQuantumBtn = document.getElementById("btn-tab-quantum");
    const canvasRadar = document.getElementById("radar-map-canvas");
    const canvasQuantum = document.getElementById("quantum-canvas");

    if (tabRadarBtn && tabQuantumBtn) {
        tabRadarBtn.addEventListener("click", () => {
            tabRadarBtn.classList.add("active");
            tabQuantumBtn.classList.remove("active");
            canvasRadar.classList.add("active");
            canvasQuantum.classList.remove("active");
            resizeCanvases();
        });

        tabQuantumBtn.addEventListener("click", () => {
            tabQuantumBtn.classList.add("active");
            tabRadarBtn.classList.remove("active");
            canvasQuantum.classList.add("active");
            canvasRadar.classList.remove("active");
            resizeCanvases();
        });
    }

    // --------------------------------------------------
    // Canvas Sizing
    // --------------------------------------------------
    const pCanvas = document.getElementById("particle-canvas");
    const pCtx = pCanvas.getContext("2d");
    const qCanvas = document.getElementById("quantum-canvas");
    const qCtx = qCanvas.getContext("2d");
    const rCanvas = document.getElementById("radar-map-canvas");
    const rCtx = rCanvas.getContext("2d");

    function resizeCanvases() {
        pCanvas.width = window.innerWidth;
        pCanvas.height = window.innerHeight;
        
        if (qCanvas.classList.contains("active")) {
            qCanvas.width = qCanvas.clientWidth;
            qCanvas.height = qCanvas.clientHeight;
        }
        if (rCanvas.classList.contains("active")) {
            rCanvas.width = rCanvas.clientWidth;
            rCanvas.height = rCanvas.clientHeight;
        }
    }
    window.addEventListener("resize", resizeCanvases);
    // Initial trigger
    pCanvas.width = window.innerWidth;
    pCanvas.height = window.innerHeight;
    rCanvas.width = rCanvas.clientWidth;
    rCanvas.height = rCanvas.clientHeight;
    qCanvas.width = qCanvas.clientWidth;
    qCanvas.height = qCanvas.clientHeight;

    // --------------------------------------------------
    // Background Particle System
    // --------------------------------------------------
    let particles = [];
    class Particle {
        constructor() {
            this.reset();
        }
        reset() {
            this.x = Math.random() * pCanvas.width;
            this.y = pCanvas.height + Math.random() * 50;
            this.size = Math.random() * 1.2 + 0.4;
            this.speedY = -(Math.random() * 0.3 + 0.1);
            this.speedX = (Math.random() * 0.16 - 0.08);
            this.color = Math.random() > 0.5 
                ? "rgba(0, 229, 255, " + (Math.random() * 0.2 + 0.05) + ")" 
                : "rgba(217, 70, 239, " + (Math.random() * 0.2 + 0.05) + ")";
        }
        update() {
            this.y += this.speedY;
            this.x += this.speedX;
            if (this.y < -10) {
                this.reset();
            }
        }
        draw() {
            pCtx.fillStyle = this.color;
            pCtx.beginPath();
            pCtx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            pCtx.fill();
        }
    }

    for (let i = 0; i < 30; i++) {
        particles.push(new Particle());
    }

    function animateParticles() {
        pCtx.clearRect(0, 0, pCanvas.width, pCanvas.height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animateParticles);
    }
    animateParticles();

    // --------------------------------------------------
    // Mini Waveforms inside Sensor Cards (Canvas)
    // --------------------------------------------------
    const waveforms = [
        { id: "radar-wave", color: "#00E5FF", freq: 0.15, amp: 6, phase: 0 },
        { id: "infrared-wave", color: "#3B82F6", freq: 0.1, amp: 4, phase: 0 },
        { id: "thermal-wave", color: "#D946EF", freq: 0.2, amp: 5, phase: 0 },
        { id: "acoustic-wave", color: "#F59E0B", freq: 0.08, amp: 7, phase: 0 }
    ];

    waveforms.forEach(wave => {
        const cv = document.getElementById(wave.id);
        if (cv) {
            wave.canvas = cv;
            wave.ctx = cv.getContext("2d");
            cv.width = cv.clientWidth;
            cv.height = cv.clientHeight;
        }
    });

    // Make waves responsive
    window.addEventListener("resize", () => {
        waveforms.forEach(wave => {
            if (wave.canvas) {
                wave.canvas.width = wave.canvas.clientWidth;
                wave.canvas.height = wave.canvas.clientHeight;
            }
        });
    });

    function drawWaveforms() {
        waveforms.forEach(wave => {
            if (!wave.canvas || !wave.ctx) return;
            const ctx = wave.ctx;
            const w = wave.canvas.width;
            const h = wave.canvas.height;
            
            ctx.clearRect(0, 0, w, h);
            ctx.strokeStyle = wave.color;
            ctx.lineWidth = 1;
            ctx.beginPath();
            
            for (let x = 0; x < w; x++) {
                let factor = 1;
                if (wave.id.includes("radar")) factor = state.sensorValues.Radar / 100;
                if (wave.id.includes("infrared")) factor = state.sensorValues.Infrared / 100;
                if (wave.id.includes("thermal")) factor = state.sensorValues.Thermal / 100;
                if (wave.id.includes("acoustic")) factor = state.sensorValues.Acoustic / 100;

                const y = h/2 + Math.sin(x * wave.freq + wave.phase) * (wave.amp * factor);
                if (x === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            ctx.stroke();
            wave.phase += 0.06;
        });
        requestAnimationFrame(drawWaveforms);
    }
    drawWaveforms();

    // --------------------------------------------------
    // Battlespace Radar Scope (Canvas)
    // --------------------------------------------------
    function drawRadarScope() {
        if (!rCanvas.classList.contains("active")) {
            requestAnimationFrame(drawRadarScope);
            return;
        }

        const w = rCanvas.width;
        const h = rCanvas.height;
        const cx = w / 2;
        const cy = h / 2;
        const maxRadius = Math.min(w, h) * 0.45;

        rCtx.clearRect(0, 0, w, h);

        // 1. Draw Concentric Grid Rings
        rCtx.strokeStyle = "rgba(0, 229, 255, 0.08)";
        rCtx.lineWidth = 1;
        const ringCount = 4;
        for (let i = 1; i <= ringCount; i++) {
            const r = (maxRadius / ringCount) * i;
            rCtx.beginPath();
            rCtx.arc(cx, cy, r, 0, Math.PI * 2);
            rCtx.stroke();

            // Distance labels
            rCtx.fillStyle = "rgba(0, 229, 255, 0.3)";
            rCtx.font = "8px 'Share Tech Mono'";
            rCtx.textAlign = "center";
            rCtx.fillText(`${Math.round(state.environment.visibility * 8 * (i/ringCount))}KM`, cx, cy - r + 3);
        }

        // 2. Draw Crosshair Axis Lines
        rCtx.strokeStyle = "rgba(0, 229, 255, 0.05)";
        rCtx.setLineDash([4, 4]);
        rCtx.beginPath();
        rCtx.moveTo(cx - maxRadius, cy);
        rCtx.lineTo(cx + maxRadius, cy);
        rCtx.moveTo(cx, cy - maxRadius);
        rCtx.lineTo(cx, cy + maxRadius);
        rCtx.stroke();
        rCtx.setLineDash([]); // Reset

        // 3. Draw Conic Radar Sweep
        radarState.angle += 0.01;
        if (radarState.angle > Math.PI * 2) radarState.angle = 0;

        rCtx.save();
        rCtx.translate(cx, cy);
        rCtx.rotate(radarState.angle);
        
        // Conic gradient sweep
        const sweepGrad = rCtx.createConicGradient(0, 0, 0);
        sweepGrad.addColorStop(0, "rgba(0, 229, 255, 0.18)");
        sweepGrad.addColorStop(0.15, "rgba(0, 229, 255, 0.02)");
        sweepGrad.addColorStop(0.5, "rgba(0, 229, 255, 0)");
        sweepGrad.addColorStop(1, "rgba(0, 229, 255, 0)");

        rCtx.fillStyle = sweepGrad;
        rCtx.beginPath();
        rCtx.moveTo(0, 0);
        rCtx.arc(0, 0, maxRadius, 0, Math.PI * 2);
        rCtx.fill();

        // Sweeping leading line
        rCtx.strokeStyle = "rgba(0, 229, 255, 0.5)";
        rCtx.lineWidth = 1.5;
        rCtx.beginPath();
        rCtx.moveTo(0, 0);
        rCtx.lineTo(maxRadius, 0);
        rCtx.stroke();
        rCtx.restore();

        // 4. Draw Active Target Markers (Threat blips)
        // If threat level is Low (no target detected), no active target blip is rendered
        if (state.threatLevel !== "LOW") {
            const targetX = cx + Math.cos(-Math.PI / 4) * (maxRadius * 0.6);
            const targetY = cy + Math.sin(-Math.PI / 4) * (maxRadius * 0.6);

            // Pulsing target halo
            const pulseSize = 10 + Math.sin(Date.now() * 0.008) * 4;
            rCtx.strokeStyle = "rgba(239, 68, 68, 0.6)";
            rCtx.lineWidth = 1;
            rCtx.beginPath();
            rCtx.arc(targetX, targetY, pulseSize, 0, Math.PI * 2);
            rCtx.stroke();

            // Core Blip
            rCtx.fillStyle = "var(--danger-color)";
            rCtx.beginPath();
            rCtx.arc(targetX, targetY, 4, 0, Math.PI * 2);
            rCtx.shadowBlur = 6;
            rCtx.shadowColor = "var(--danger-color)";
            rCtx.fill();
            rCtx.shadowBlur = 0; // Reset

            // Locked Crosshairs (Rotating square around blip)
            rCtx.save();
            rCtx.translate(targetX, targetY);
            rCtx.rotate(Date.now() * 0.002);
            rCtx.strokeStyle = "var(--danger-color)";
            rCtx.lineWidth = 1;
            rCtx.strokeRect(-8, -8, 16, 16);
            rCtx.restore();

            // Target details readout
            rCtx.fillStyle = "#FFFFFF";
            rCtx.font = "bold 9px 'Share Tech Mono'";
            rCtx.textAlign = "left";
            rCtx.fillText("TRG_01 [LOCKED]", targetX + 12, targetY - 4);
            rCtx.fillStyle = "var(--danger-color)";
            rCtx.fillText(`CONF: ${state.threatConfidence}%`, targetX + 12, targetY + 6);
            rCtx.fillStyle = "var(--text-muted)";
            rCtx.fillText(`R: ${(state.environment.visibility * 4.5).toFixed(1)}KM  B: 45°`, targetX + 12, targetY + 16);
        } else {
            // Draw dummy scanning target coordinate indicator
            rCtx.fillStyle = "rgba(0, 229, 255, 0.4)";
            rCtx.font = "9px 'Share Tech Mono'";
            rCtx.textAlign = "center";
            rCtx.fillText("SCANNING AREA CLEAR // NO TARGETS LOCKED", cx, cy + maxRadius + 18);
        }

        requestAnimationFrame(drawRadarScope);
    }
    // Start radar map draw loop
    drawRadarScope();

    // --------------------------------------------------
    // Quantum Node Network (Canvas)
    // --------------------------------------------------
    const nodes = [
        { id: "s1", name: "RADAR", type: "sensor", key: "Radar", xPct: 0.15, yPct: 0.2, active: true },
        { id: "s2", name: "INFRARED", type: "sensor", key: "Infrared", xPct: 0.15, yPct: 0.4, active: false },
        { id: "s3", name: "THERMAL", type: "sensor", key: "Thermal", xPct: 0.15, yPct: 0.6, active: true },
        { id: "s4", name: "ACOUSTIC", type: "sensor", key: "Acoustic", xPct: 0.15, yPct: 0.8, active: true },
        { id: "q1", name: "QUBIT_0", type: "qubit", xPct: 0.5, yPct: 0.35, active: true },
        { id: "q2", name: "QUBIT_1", type: "qubit", xPct: 0.5, yPct: 0.65, active: true },
        { id: "o1", name: "THREAT_CLASSIFIER", type: "output", xPct: 0.85, yPct: 0.35, active: true },
        { id: "o2", name: "TACTICAL_ACTION", type: "output", xPct: 0.85, yPct: 0.65, active: true }
    ];

    const connections = [
        { from: "s1", to: "q1", pulseSpeed: 0.015, pos: 0, active: true },
        { from: "s2", to: "q1", pulseSpeed: 0.01, pos: 0, active: false },
        { from: "s3", to: "q2", pulseSpeed: 0.02, pos: 0, active: true },
        { from: "s4", to: "q2", pulseSpeed: 0.012, pos: 0, active: true },
        { from: "q1", to: "o1", pulseSpeed: 0.025, pos: 0, active: true },
        { from: "q2", to: "o1", pulseSpeed: 0.02, pos: 0, active: true },
        { from: "q1", to: "o2", pulseSpeed: 0.018, pos: 0, active: true },
        { from: "q2", to: "o2", pulseSpeed: 0.022, pos: 0, active: true }
    ];

    function drawQuantumNetwork() {
        if (!qCanvas.classList.contains("active")) {
            requestAnimationFrame(drawQuantumNetwork);
            return;
        }

        const w = qCanvas.width;
        const h = qCanvas.height;
        qCtx.clearRect(0, 0, w, h);
        
        // Sync active flags
        nodes.forEach(n => {
            if (n.type === "sensor") {
                n.active = state.selection[n.key] === 1;
            }
        });

        connections.forEach(c => {
            const fromNode = nodes.find(n => n.id === c.from);
            c.active = fromNode ? fromNode.active : true;
        });

        // 1. Draw connections
        connections.forEach(conn => {
            const fromNode = nodes.find(n => n.id === conn.from);
            const toNode = nodes.find(n => n.id === conn.to);
            if (!fromNode || !toNode) return;

            const x1 = fromNode.xPct * w;
            const y1 = fromNode.yPct * h;
            const x2 = toNode.xPct * w;
            const y2 = toNode.yPct * h;

            qCtx.strokeStyle = conn.active 
                ? "rgba(0, 229, 255, 0.35)" 
                : "rgba(255, 255, 255, 0.04)";
            qCtx.lineWidth = conn.active ? 1.5 : 1;
            
            qCtx.beginPath();
            qCtx.moveTo(x1, y1);
            qCtx.lineTo(x2, y2);
            qCtx.stroke();

            // Draw pulses
            if (conn.active) {
                conn.pos += conn.pulseSpeed;
                if (conn.pos > 1) conn.pos = 0;

                const pulseX = x1 + (x2 - x1) * conn.pos;
                const pulseY = y1 + (y2 - y1) * conn.pos;

                qCtx.fillStyle = "#D946EF";
                qCtx.beginPath();
                qCtx.arc(pulseX, pulseY, 3, 0, Math.PI * 2);
                qCtx.shadowBlur = 6;
                qCtx.shadowColor = "#D946EF";
                qCtx.fill();
                qCtx.shadowBlur = 0;
            }
        });

        // 2. Draw Nodes
        nodes.forEach(node => {
            const x = node.xPct * w;
            const y = node.yPct * h;
            
            let color = "rgba(100, 116, 139, 0.4)";
            let glow = "transparent";
            let radius = 8;

            if (node.active) {
                if (node.type === "sensor") {
                    color = "#00E5FF";
                    glow = "rgba(0, 229, 255, 0.4)";
                } else if (node.type === "qubit") {
                    color = "#D946EF";
                    glow = "rgba(217, 70, 239, 0.4)";
                    radius = 10;
                } else {
                    color = "#22C55E";
                    glow = "rgba(34, 197, 94, 0.4)";
                }
            }

            if (node.active) {
                const pulseRadius = radius + Math.sin(Date.now() * 0.005) * 3;
                qCtx.strokeStyle = glow;
                qCtx.lineWidth = 1;
                qCtx.beginPath();
                qCtx.arc(x, y, pulseRadius, 0, Math.PI * 2);
                qCtx.stroke();
            }

            qCtx.fillStyle = color;
            qCtx.beginPath();
            qCtx.arc(x, y, radius, 0, Math.PI * 2);
            qCtx.shadowBlur = node.active ? 6 : 0;
            qCtx.shadowColor = color;
            qCtx.fill();
            qCtx.shadowBlur = 0;

            qCtx.fillStyle = "#050816";
            qCtx.beginPath();
            qCtx.arc(x, y, radius - 3, 0, Math.PI * 2);
            qCtx.fill();

            qCtx.font = "bold 8.5px 'Share Tech Mono'";
            qCtx.fillStyle = node.active ? "#FFF" : "rgba(255,255,255,0.25)";
            qCtx.textAlign = "center";
            qCtx.fillText(node.name, x, y - radius - 5);
        });

        requestAnimationFrame(drawQuantumNetwork);
    }
    drawQuantumNetwork();

    // --------------------------------------------------
    // Event Logs scrolling terminal
    // --------------------------------------------------
    const logTerminal = document.getElementById("log-terminal-feed");
    
    function logEvent(tag, message) {
        if (!logTerminal) return;
        
        const timestamp = formatTime(new Date());
        const logRow = document.createElement("div");
        logRow.className = "log-row";
        
        let tagColor = "text-cyan";
        if (tag === "DETECTION" || tag === "WARNING") tagColor = "text-red";
        if (tag === "QUANTUM") tagColor = "text-magenta";
        if (tag === "SYSTEM") tagColor = "text-blue";

        logRow.innerHTML = `
            <span class="log-time">[${timestamp}]</span>
            <span class="log-tag ${tagColor}">[${tag}]</span>
            <span class="log-text">${message}</span>
        `;
        
        logTerminal.appendChild(logRow);
        logTerminal.scrollTop = logTerminal.scrollHeight;
        
        while (logTerminal.children.length > 30) {
            logTerminal.removeChild(logTerminal.firstChild);
        }
    }

    logEvent("SYSTEM", "Multi-spectral pipeline streamlined successfully.");
    logEvent("QUANTUM", "Active connection to QPU solver solved.");
    logEvent("SYSTEM", "Awaiting sensor sweeps...");

    // --------------------------------------------------
    // Chart.js Setup (Unified & Minimal)
    // --------------------------------------------------
    
    // 1. Line Chart: Detection Confidence History
    const ctxLine = document.getElementById("lineChart").getContext("2d");
    const lineChart = new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: ['-30s', '-24s', '-18s', '-12s', '-6s', 'NOW'],
            datasets: [{
                label: 'Confidence',
                data: state.confidenceHistory,
                borderColor: '#00E5FF',
                backgroundColor: 'rgba(0, 229, 255, 0.05)',
                fill: true,
                tension: 0.4,
                borderWidth: 1.5,
                pointRadius: 2,
                pointBackgroundColor: '#00E5FF'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { color: '#64748B', font: { family: 'Share Tech Mono', size: 8 } }
                },
                y: {
                    min: 0,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { color: '#64748B', font: { family: 'Share Tech Mono', size: 8 } }
                }
            }
        }
    });

    // 2. Bar Chart: Weights comparison
    const ctxBar = document.getElementById("barChart").getContext("2d");
    const barChart = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: ['Radar', 'IR', 'Thermal', 'Sonar'],
            datasets: [
                {
                    label: 'Quantum Weight',
                    data: [40, 0, 35, 25],
                    backgroundColor: 'rgba(217, 70, 239, 0.4)',
                    borderColor: '#D946EF',
                    borderWidth: 1,
                    borderRadius: 1
                },
                {
                    label: 'Classical Weight',
                    data: [40, 30, 0, 30],
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    borderColor: '#3B82F6',
                    borderWidth: 1,
                    borderRadius: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#64748B', font: { family: 'Share Tech Mono', size: 8 } }
                },
                y: {
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { color: '#64748B', font: { family: 'Share Tech Mono', size: 8 } }
                }
            }
        }
    });

    // --------------------------------------------------
    // Live UI Render Helpers
    // --------------------------------------------------
    function updateSVGProgressRing(circleId, percentage, radius = 34) {
        const circle = document.getElementById(circleId);
        if (!circle) return;
        const circumference = 2 * Math.PI * radius;
        circle.style.strokeDasharray = `${circumference}`;
        const offset = circumference - (percentage / 100) * circumference;
        circle.style.strokeDashoffset = offset;
    }

    function renderUI() {
        // 1. Update Live Sensor Cards values
        document.getElementById("radar-confidence-val").textContent = `${state.sensorValues.Radar}%`;
        updateSVGProgressRing("gauge-radar", state.sensorValues.Radar);
        
        document.getElementById("infrared-confidence-val").textContent = `${state.sensorValues.Infrared}%`;
        updateSVGProgressRing("gauge-infrared", state.sensorValues.Infrared);

        document.getElementById("thermal-confidence-val").textContent = `${state.sensorValues.Thermal}%`;
        updateSVGProgressRing("gauge-thermal", state.sensorValues.Thermal);

        document.getElementById("acoustic-confidence-val").textContent = `${state.sensorValues.Acoustic}%`;
        updateSVGProgressRing("gauge-acoustic", state.sensorValues.Acoustic);

        for (const [key, value] of Object.entries(state.sensorStatus)) {
            const statusEl = document.getElementById(`${key.toLowerCase()}-status`);
            if (statusEl) {
                statusEl.textContent = value;
                statusEl.className = `sensor-status ${value === 'ONLINE' ? 'status-online' : 'status-warning'}`;
            }
        }

        // 2. Quantum variables displays
        document.getElementById("var-radar").textContent = state.selection.Radar;
        document.getElementById("var-infrared").textContent = state.selection.Infrared;
        document.getElementById("var-thermal").textContent = state.selection.Thermal;
        document.getElementById("var-acoustic").textContent = state.selection.Acoustic;

        const bestVector = `${state.selection.Radar} ${state.selection.Infrared} ${state.selection.Thermal} ${state.selection.Acoustic}`;
        document.getElementById("best-vector-display").textContent = bestVector;
        document.getElementById("qubo-energy").textContent = state.qubo.energy.toFixed(3);
        document.getElementById("qubo-iteration").textContent = state.qubo.iteration.toLocaleString();

        // 3. Threat analysis panel
        document.getElementById("threat-confidence-val").textContent = `${state.threatConfidence}%`;
        updateSVGProgressRing("threat-confidence-gauge", state.threatConfidence, 42);
        
        const threatLevelEl = document.getElementById("threat-level");
        const actionEl = document.getElementById("recommended-action");
        if (threatLevelEl) {
            threatLevelEl.textContent = state.threatLevel;
            threatLevelEl.className = "value";
            if (state.threatLevel === "CRITICAL" || state.threatLevel === "HIGH") {
                threatLevelEl.classList.add("text-red", "animate-pulse-fast");
            } else if (state.threatLevel === "MEDIUM") {
                threatLevelEl.classList.add("text-amber");
            } else {
                threatLevelEl.classList.add("text-cyan");
            }
        }

        if (actionEl) {
            actionEl.textContent = state.recommendedAction;
            actionEl.className = "action-badge";
            if (state.recommendedAction === "INTERCEPT") {
                actionEl.classList.add("bg-red");
            } else if (state.recommendedAction === "TRACK") {
                actionEl.classList.add("bg-amber");
            } else {
                actionEl.classList.add("bg-cyan");
            }
        }

        // 4. Environment values
        document.getElementById("env-weather").textContent = state.environment.weather;
        document.getElementById("env-visibility").textContent = `${state.environment.visibility} KM`;
        document.getElementById("env-noise").textContent = `${state.environment.noise} dB`;
        document.getElementById("env-wind").textContent = `${state.environment.wind} Kts`;
        document.getElementById("env-temp").textContent = `${state.environment.temp}°C`;
        document.getElementById("env-stealth").textContent = state.environment.stealth.toFixed(2);

        // 5. System metrics (Inlined in Header)
        document.getElementById("cpu-telemetry-val").textContent = `${state.systemMetrics.cpu}%`;
        document.getElementById("mem-telemetry-val").textContent = `${state.systemMetrics.mem}%`;
        document.getElementById("qpu-telemetry-val").textContent = `${state.systemMetrics.qpu}%`;

        // 6. Charts update
        lineChart.data.datasets[0].data = state.confidenceHistory;
        lineChart.update('none');

        // Update Bar weights
        const qWeights = getNormalizedWeights(state.selection);
        // Classical selection averages all active sensors
        const cSelection = { Radar: 1, Infrared: 1, Thermal: 0, Acoustic: 1 };
        const cWeights = getNormalizedWeights(cSelection);

        barChart.data.datasets[0].data = qWeights;
        barChart.data.datasets[1].data = cWeights;
        barChart.update('none');
    }

    function getNormalizedWeights(selectionVector) {
        let wRadar = selectionVector.Radar ? state.sensorValues.Radar : 0;
        let wIR = selectionVector.Infrared ? state.sensorValues.Infrared : 0;
        let wThermal = selectionVector.Thermal ? state.sensorValues.Thermal : 0;
        let wSonar = selectionVector.Acoustic ? state.sensorValues.Acoustic : 0;
        const total = wRadar + wIR + wThermal + wSonar;
        if (total === 0) return [25, 25, 25, 25];
        return [
            Math.round((wRadar / total) * 100),
            Math.round((wIR / total) * 100),
            Math.round((wThermal / total) * 100),
            Math.round((wSonar / total) * 100)
        ];
    }

    // --------------------------------------------------
    // Live Simulation Loop (Pipeline Sweep)
    // --------------------------------------------------
    const pipelineSequence = [
        "pipe-input",
        "pipe-sync",
        "pipe-features",
        "pipe-ai",
        "pipe-quantum",
        "pipe-threat",
        "pipe-decision"
    ];

    let currentPipelineIndex = 0;

    function runPipelineCycle() {
        pipelineSequence.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.className = "pipeline-node";
        });

        currentPipelineIndex = 0;
        
        function nextPipelineStep() {
            if (currentPipelineIndex > 0) {
                const prevEl = document.getElementById(pipelineSequence[currentPipelineIndex - 1]);
                if (prevEl) {
                    prevEl.className = "pipeline-node active";
                }
            }

            const currentId = pipelineSequence[currentPipelineIndex];
            const currentEl = document.getElementById(currentId);
            if (currentEl) {
                currentEl.className = "pipeline-node processing";
            }

            // Log corresponding details
            if (currentId === "pipe-input") {
                logEvent("SYSTEM", "Sensory nodes active. Streaming multi-spectral feeds.");
            } else if (currentId === "pipe-sync") {
                logEvent("SYSTEM", "Feeds synchronized. Jitter: < 0.1ps.");
            } else if (currentId === "pipe-features") {
                logEvent("SYSTEM", "Feature extraction complete. Stealth coefficient calculated.");
            } else if (currentId === "pipe-ai") {
                logEvent("SYSTEM", "Neural net inference complete. AI confidence generated.");
            } else if (currentId === "pipe-quantum") {
                logEvent("QUANTUM", `QUBO optimizer compiled. QPU energy: ${state.qubo.energy.toFixed(3)}`);
            } else if (currentId === "pipe-threat") {
                logEvent("DETECTION", `Target probability confirmed: ${state.threatConfidence}%`);
            } else if (currentId === "pipe-decision") {
                logEvent("DETECTION", `Tactical state matched. Recommending: ${state.recommendedAction}.`);
            }

            currentPipelineIndex++;

            if (currentPipelineIndex < pipelineSequence.length) {
                setTimeout(nextPipelineStep, 250);
            } else {
                setTimeout(() => {
                    const lastEl = document.getElementById(pipelineSequence[pipelineSequence.length - 1]);
                    if (lastEl) lastEl.className = "pipeline-node active";

                    updateSimulationState();
                }, 250);
            }
        }

        nextPipelineStep();
    }

    function updateSimulationState() {
        if (window.location.protocol.startsWith('http')) {
            // Fetch dynamically from Flask backend API
            fetch('/api/telemetry')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        state.sensorValues = data.sensorValues;
                        state.selection = data.selection;
                        state.threatConfidence = data.threatConfidence;
                        state.threatLevel = data.threatLevel;
                        state.recommendedAction = data.recommendedAction;
                        state.environment = data.environment;
                        
                        if (data.qubo) {
                            state.qubo.energy = data.qubo.energy;
                            state.qubo.iteration = data.qubo.iteration;
                        }

                        // Update comparison visual bars from actual backend values
                        if (data.benchmarks) {
                            animateComparisonBars(data.benchmarks);
                        }

                        // Generate plain english briefing dynamically
                        composeBriefingText();

                        state.confidenceHistory.shift();
                        state.confidenceHistory.push(state.threatConfidence);

                        renderUI();
                    }
                })
                .catch(err => {
                    console.error("API link offline, running mock simulation", err);
                    runMockUpdate();
                    composeBriefingText();
                    renderUI();
                });
        } else {
            runMockUpdate();
            composeBriefingText();
            renderUI();
        }
    }

    function runMockUpdate() {
        state.sensorValues.Radar = Math.max(30, Math.min(98, state.sensorValues.Radar + Math.floor(Math.random() * 11) - 5));
        state.sensorValues.Infrared = Math.max(20, Math.min(95, state.sensorValues.Infrared + Math.floor(Math.random() * 9) - 4));
        state.sensorValues.Thermal = Math.max(40, Math.min(99, state.sensorValues.Thermal + Math.floor(Math.random() * 13) - 6));
        state.sensorValues.Acoustic = Math.max(10, Math.min(80, state.sensorValues.Acoustic + Math.floor(Math.random() * 15) - 7));

        state.sensorStatus.Radar = Math.random() > 0.90 ? "WARNING" : "ONLINE";
        state.sensorStatus.Acoustic = Math.random() > 0.85 ? "WARNING" : "ONLINE";

        let weatherProb = Math.random();
        if (weatherProb < 0.33) {
            state.environment.weather = "CLEAR";
            state.environment.visibility = 8.5;
            state.environment.noise = Math.max(30, Math.min(50, state.environment.noise + Math.floor(Math.random() * 7) - 3));
            
            state.selection.Radar = 1;
            state.selection.Infrared = 1;
            state.selection.Thermal = 0;
            state.selection.Acoustic = 0;
            state.qubo.energy = -3.124;
        } else if (weatherProb < 0.66) {
            state.environment.weather = "RAINY";
            state.environment.visibility = 3.4;
            state.environment.noise = Math.max(60, Math.min(85, state.environment.noise + Math.floor(Math.random() * 9) - 4));
            
            state.selection.Radar = 0;
            state.selection.Infrared = 0;
            state.selection.Thermal = 1;
            state.selection.Acoustic = 1;
            state.qubo.energy = -2.482;
        } else {
            state.environment.weather = "FOGGY";
            state.environment.visibility = 1.1;
            state.environment.noise = Math.max(50, Math.min(75, state.environment.noise + Math.floor(Math.random() * 5) - 2));
            
            state.selection.Radar = 1;
            state.selection.Infrared = 0;
            state.selection.Thermal = 1;
            state.selection.Acoustic = 1;
            state.qubo.energy = -2.895;
        }

        state.qubo.iteration = Math.floor(state.qubo.iteration + (Math.random() * 40 - 20));

        let selectedCount = 0;
        let weightedScoreSum = 0;
        if (state.selection.Radar) { selectedCount++; weightedScoreSum += state.sensorValues.Radar; }
        if (state.selection.Infrared) { selectedCount++; weightedScoreSum += state.sensorValues.Infrared; }
        if (state.selection.Thermal) { selectedCount++; weightedScoreSum += state.sensorValues.Thermal; }
        if (state.selection.Acoustic) { selectedCount++; weightedScoreSum += state.sensorValues.Acoustic; }

        let baseConfidence = selectedCount > 0 ? (weightedScoreSum / selectedCount) : 40;
        state.environment.stealth = Math.max(0.1, Math.min(0.99, state.environment.stealth + (Math.random() * 0.08 - 0.04)));
        let actualConfidence = Math.max(10, Math.min(99, Math.round(baseConfidence * (1.1 - state.environment.stealth / 3))));
        
        state.threatConfidence = actualConfidence;

        if (state.threatConfidence >= 85) {
            state.threatLevel = "CRITICAL";
            state.recommendedAction = "INTERCEPT";
        } else if (state.threatConfidence >= 65) {
            state.threatLevel = "HIGH";
            state.recommendedAction = "TRACK";
        } else if (state.threatConfidence >= 40) {
            state.threatLevel = "MEDIUM";
            state.recommendedAction = "MONITOR";
        } else {
            state.threatLevel = "LOW";
            state.recommendedAction = "IGNORE";
        }

        state.environment.wind = Math.max(5, Math.min(45, state.environment.wind + Math.floor(Math.random() * 5) - 2));
        state.environment.temp = Math.max(12, Math.min(32, state.environment.temp + Math.floor(Math.random() * 3) - 1));

        state.systemMetrics.cpu = Math.max(15, Math.min(90, Math.floor(35 + Math.random() * 20 - 10)));
        state.systemMetrics.mem = Math.max(40, Math.min(95, Math.floor(52 + Math.random() * 6 - 3)));
        state.systemMetrics.qpu = Math.max(60, Math.min(98, Math.floor(78 + Math.random() * 10 - 5)));
        state.systemMetrics.inferenceTime = 1.0 + Math.random() * 0.5;
        state.systemMetrics.latency = 3.5 + Math.random() * 2.5;

        // Mock benchmarks
        const classAcc = Math.round(state.threatConfidence * 0.82);
        const classAlarm = Math.round(15 - state.threatConfidence / 12);
        const classLat = Math.round(40 + state.environment.noise * 0.2);

        const mockBenchmarks = {
            classical: {
                accuracy: `${classAcc}.5%`,
                falseAlarm: `${classAlarm}.4%`,
                latency: `${classLat}.0ms`
            },
            quantum: {
                accuracy: `${state.threatConfidence}.0%`,
                falseAlarm: `${(classAlarm * 0.15).toFixed(1)}%`,
                latency: `${state.systemMetrics.inferenceTime.toFixed(1)}ms`
            }
        };

        animateComparisonBars(mockBenchmarks);

        state.confidenceHistory.shift();
        state.confidenceHistory.push(state.threatConfidence);
    }

    function animateComparisonBars(benchmarks) {
        // Parse raw values
        const clAcc = parseFloat(benchmarks.classical.accuracy);
        const qAcc = parseFloat(benchmarks.quantum.accuracy);
        const clAlarm = parseFloat(benchmarks.classical.falseAlarm);
        const qAlarm = parseFloat(benchmarks.quantum.falseAlarm);
        const clLat = parseFloat(benchmarks.classical.latency);
        const qLat = parseFloat(benchmarks.quantum.latency);

        // Map widths
        document.getElementById("bar-classic-acc").style.width = `${clAcc}%`;
        document.getElementById("bar-quantum-acc").style.width = `${qAcc}%`;
        document.getElementById("bar-classic-alarm").style.width = `${clAlarm * 3}%`; // scaled for visual distinction
        document.getElementById("bar-quantum-alarm").style.width = `${qAlarm * 3}%`;
        document.getElementById("bar-classic-lat").style.width = `90%`;
        document.getElementById("bar-quantum-lat").style.width = `${Math.max(5, Math.min(25, (qLat / clLat) * 90))}%`;

        // Update readouts
        document.getElementById("val-classic-acc").textContent = benchmarks.classical.accuracy;
        document.getElementById("val-quantum-acc").textContent = benchmarks.quantum.accuracy;
        document.getElementById("val-classic-alarm").textContent = benchmarks.classical.falseAlarm;
        document.getElementById("val-quantum-alarm").textContent = benchmarks.quantum.falseAlarm;
        document.getElementById("val-classic-lat").textContent = benchmarks.classical.latency;
        document.getElementById("val-quantum-lat").textContent = benchmarks.quantum.latency;

        // Delta
        const diff = qAcc - clAcc;
        document.getElementById("quantum-delta-percentage").textContent = `+${diff.toFixed(1)}%`;
    }

    function composeBriefingText() {
        const briefingEl = document.getElementById("judge-briefing-text");
        if (!briefingEl) return;

        let selectedNames = [];
        if (state.selection.Radar) selectedNames.push("RADAR");
        if (state.selection.Infrared) selectedNames.push("INFRARED");
        if (state.selection.Thermal) selectedNames.push("THERMAL");
        if (state.selection.Acoustic) selectedNames.push("SONAR");

        const selectionStr = selectedNames.join(" + ");
        
        let text = "";
        if (state.threatLevel === "LOW") {
            text = `<strong>BATTLESPACE STATUS: NORMAL.</strong> Scanner sweep reports no threat signatures. Sector 4 environment is ${state.environment.weather.toLowerCase()} with a visibility of ${state.environment.visibility}KM. Quantum optimization is running in standby, keeping background telemetry clean.`;
        } else {
            text = `<strong>CRITICAL INTRUSION:</strong> A target (stealth index: <strong>${state.environment.stealth.toFixed(2)}</strong>) was detected. Due to ${state.environment.weather.toLowerCase()} weather and ambient noise (${state.environment.noise}dB), classical weighted averaging got confused (accuracy: ${document.getElementById("val-classic-acc").textContent}). The D-Wave Quantum solver formulated a QUBO Ising configuration, instantly selecting <strong>[${selectionStr}]</strong>. This bypassed the sensor noise and locked the target with <strong>${state.threatConfidence}%</strong> confidence, calling for an immediate <strong>${state.recommendedAction}</strong> action.`;
        }

        briefingEl.innerHTML = text;
    }

    // --------------------------------------------------
    // Initial Render & Cycle Start
    // --------------------------------------------------
    renderUI();
    
    // Run the pipeline loop every 4.5 seconds
    setInterval(runPipelineCycle, 4500);
    setTimeout(runPipelineCycle, 1000);
});
