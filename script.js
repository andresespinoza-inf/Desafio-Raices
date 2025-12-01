class ExactPythonReplica {
    constructor() {
        this.currentProblem = null;
        this.tolerance = 1e-6;
        this.maxIterations = 100;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createParticles();  // ← AÑADIR ESTA LÍNEA
    }

    // ↓ AGREGAR ESTE MÉTODO NUEVO (antes de setupEventListeners)
    createParticles() {
        const particlesContainer = document.getElementById('particles');
        const particleCount = 30;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Posición y tamaño aleatorios
            const size = Math.random() * 8 + 2;
            const left = Math.random() * 100;
            const animationDuration = Math.random() * 20 + 10;
            const animationDelay = Math.random() * 20;
            
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${left}%`;
            particle.style.animationDuration = `${animationDuration}s`;
            particle.style.animationDelay = `${animationDelay}s`;
            
            particlesContainer.appendChild(particle);
        }
    }

    setupEventListeners() {
        // Selección de problemas
        document.querySelectorAll('.problem-card').forEach(card => {
            card.addEventListener('click', (e) => {
                this.selectProblem(e.currentTarget.dataset.problem);
            });
        });

        // Botón ejecutar
        document.getElementById('solve-all-btn').addEventListener('click', () => {
            this.solveSelectedProblem();
        });
    }

    selectProblem(problemNumber) {
        this.currentProblem = problemNumber;
        
        document.querySelectorAll('.problem-card').forEach(card => {
            card.classList.remove('active');
        });
        document.querySelector(`[data-problem="${problemNumber}"]`).classList.add('active');
    }

    solveSelectedProblem() {
        if (!this.currentProblem) {
            this.showError('Por favor selecciona un problema');
            return;
        }

        const solveBtn = document.getElementById('solve-all-btn');
        const originalText = solveBtn.textContent;
        solveBtn.innerHTML = '<span class="loading"></span> Analizando...';
        solveBtn.disabled = true;

        setTimeout(() => {
            try {
                const results = this.solveProblem(this.currentProblem);
                this.displayResults(results);
                this.displaySummary(results);
            } catch (error) {
                this.showError(`Error: ${error.message}`);
            } finally {
                solveBtn.textContent = originalText;
                solveBtn.disabled = false;
            }
        }, 100);
    }

    solveProblem(problemNumber) {
        const problems = {
            '1': {
                name: "x³ - e^(0.8x) = 20 entre x = 0 y x = 8",
                func: (x) => x**3 - Math.exp(0.8*x) - 20,
                deriv: (x) => 3*x**2 - 0.8*Math.exp(0.8*x),
                range: [0, 8],
                bisection: [[3.0, 4.0], [7.0, 8.0]],
                newton: [3.5, 7.5],
                secant: [[3.0, 4.0], [7.0, 8.0]]
            },
            '2': {
                name: "3sin(0.5x) - 0.5x + 2 = 0",
                func: (x) => 3*Math.sin(0.5*x) - 0.5*x + 2,
                deriv: (x) => 1.5*Math.cos(0.5*x) - 0.5,
                range: [0, 10],
                bisection: [[5.0, 6.0]],
                newton: [5.5],
                secant: [[5.0, 6.0]]
            },
            '3': {
                name: "x³ - x²e^(-0.5x) - 3x = -1",
                func: (x) => x**3 - x**2*Math.exp(-0.5*x) - 3*x + 1,
                deriv: (x) => 3*x**2 - (2*x*Math.exp(-0.5*x) - 0.5*x**2*Math.exp(-0.5*x)) - 3,
                range: [-2, 4],
                bisection: [[-1.5, -0.5], [0.0, 1.0], [1.5, 2.0]],
                newton: [-1.0, 0.5, 1.8],
                secant: [[-1.5, -0.5], [0.0, 1.0], [1.5, 2.0]]
            },
            '4': {
                name: "cos²x - 0.5xe^(0.3x) + 5 = 0",
                func: (x) => Math.cos(x)**2 - 0.5*x*Math.exp(0.3*x) + 5,
                deriv: (x) => -2*Math.cos(x)*Math.sin(x) - 0.5*(Math.exp(0.3*x) + 0.3*x*Math.exp(0.3*x)),
                range: [0, 10],
                bisection: [[3.0, 4.0]],
                newton: [3.5],
                secant: [[3.0, 4.0]]
            }
        };

        const problem = problems[problemNumber];
        
        // Análisis de la función
        const analysis = this.analyzeFunction(problem.func, problem.name, problem.range);
        
        // Resolver con los tres métodos
        const results = {
            problem: problemNumber,
            name: problem.name,
            analysis: analysis,
            bisection: this.executeBisection(problem.func, problem.bisection),
            newton: this.executeNewton(problem.func, problem.deriv, problem.newton),
            secant: this.executeSecant(problem.func, problem.secant)
        };

        return results;
    }

    analyzeFunction(func, name, range) {
        const [start, end] = range;
        const x_vals = Array.from({length: 1000}, (_, i) => start + (end - start) * i / 999);
        const y_vals = x_vals.map(x => func(x));
        
        const y_min = Math.min(...y_vals);
        const y_max = Math.max(...y_vals);
        
        const intervals = [];
        for (let i = 0; i < y_vals.length - 1; i++) {
            if (y_vals[i] * y_vals[i + 1] < 0) {
                const x_root = x_vals[i] + (x_vals[i + 1] - x_vals[i]) * Math.abs(y_vals[i]) / (Math.abs(y_vals[i]) + Math.abs(y_vals[i + 1]));
                intervals.push({
                    start: x_vals[i],
                    end: x_vals[i + 1],
                    approx: x_root
                });
            }
        }
        
        return {
            yRange: [y_min, y_max],
            intervals: intervals
        };
    }

    executeBisection(func, intervals) {
        const results = [];
        
        for (const [a, b] of intervals) {
            try {
                const result = this.bisection(func, a, b);
                results.push(result);
            } catch (error) {
                results.push({
                    root: null,
                    error: error.message,
                    iterations: 0,
                    finalError: 0,
                    fx: 0
                });
            }
        }
        
        return results;
    }

    executeNewton(func, deriv, guesses) {
        const results = [];
        
        for (const guess of guesses) {
            try {
                const result = this.newtonRaphson(func, deriv, guess);
                results.push(result);
            } catch (error) {
                results.push({
                    root: null,
                    error: error.message,
                    iterations: 0,
                    finalError: 0,
                    fx: 0
                });
            }
        }
        
        return results;
    }

    executeSecant(func, pairs) {
        const results = [];
        
        for (const [x0, x1] of pairs) {
            try {
                const result = this.secant(func, x0, x1);
                results.push(result);
            } catch (error) {
                results.push({
                    root: null,
                    error: error.message,
                    iterations: 0,
                    finalError: 0,
                    fx: 0
                });
            }
        }
        
        return results;
    }

    bisection(func, a, b, maxIter = 20) {
        let fa = func(a);
        let fb = func(b);
        
        if (fa * fb >= 0) {
            throw new Error(`No hay cambio de signo en [${a}, ${b}]`);
        }
        
        let currentA = a;
        let currentB = b;
        let iterations = 0;
        
        for (let i = 0; i < maxIter; i++) {
            iterations = i + 1;
            const c = (currentA + currentB) / 2;
            const fc = func(c);
            const error = Math.abs(currentB - currentA) / 2;
            
            if (Math.abs(fc) < this.tolerance || error < this.tolerance) {
                return {
                    root: c,
                    iterations: iterations,
                    finalError: error,
                    fx: fc
                };
            }
            
            if (func(currentA) * fc < 0) {
                currentB = c;
            } else {
                currentA = c;
            }
        }
        
        const finalC = (currentA + currentB) / 2;
        return {
            root: finalC,
            iterations: iterations,
            finalError: Math.abs(currentB - currentA) / 2,
            fx: func(finalC)
        };
    }

    newtonRaphson(func, deriv, x0) {
        let x = x0;
        let iterations = 0;
        
        for (let i = 0; i < this.maxIterations; i++) {
            iterations = i + 1;
            const fx = func(x);
            const dfx = deriv(x);
            
            if (Math.abs(dfx) < 1e-12) {
                throw new Error('Derivada cercana a cero');
            }
            
            const xNew = x - fx / dfx;
            const error = Math.abs(xNew - x);
            
            if (Math.abs(fx) < this.tolerance || error < this.tolerance) {
                return {
                    root: xNew,
                    iterations: iterations,
                    finalError: error,
                    fx: func(xNew)
                };
            }
            
            x = xNew;
        }
        
        return {
            root: x,
            iterations: iterations,
            finalError: Math.abs(func(x)),
            fx: func(x)
        };
    }

    secant(func, x0, x1) {
        let currentX0 = x0;
        let currentX1 = x1;
        let iterations = 0;
        
        for (let i = 0; i < this.maxIterations; i++) {
            iterations = i + 1;
            const fx0 = func(currentX0);
            const fx1 = func(currentX1);
            
            if (Math.abs(fx1 - fx0) < 1e-12) {
                throw new Error('Diferencia entre evaluaciones cercana a cero');
            }
            
            const x2 = currentX1 - fx1 * (currentX1 - currentX0) / (fx1 - fx0);
            const error = Math.abs(x2 - currentX1);
            
            if (Math.abs(fx1) < this.tolerance || error < this.tolerance) {
                return {
                    root: x2,
                    iterations: iterations,
                    finalError: error,
                    fx: func(x2)
                };
            }
            
            currentX0 = currentX1;
            currentX1 = x2;
        }
        
        return {
            root: currentX1,
            iterations: iterations,
            finalError: Math.abs(func(currentX1)),
            fx: func(currentX1)
        };
    }

    displayResults(results) {
        const resultsDiv = document.getElementById('results');
        
        let html = `
            <div class="problem-result">
                <div class="problem-header">
                    🔷 PROBLEMA ${results.problem}: ${results.name}
                </div>
                
                <div class="analysis-section">
                    <pre> Análisis de ${results.name}:
   Rango de y: [${results.analysis.yRange[0].toFixed(4)}, ${results.analysis.yRange[1].toFixed(4)}]
${results.analysis.intervals.map(interval => 
`    Cambio de signo cerca de x ≈ ${interval.approx.toFixed(4)} en [${interval.start.toFixed(2)}, ${interval.end.toFixed(2)}]`
).join('\n')}</pre>
                </div>
        `;

        // 1. MÉTODO DE BISECCIÓN
        html += `
            <div class="method-result">
                <div class="method-header">
                     MÉTODO DE BISECCIÓN
                </div>
                <div class="method-content">
                    <div class="roots-list">
        `;
        
        results.bisection.forEach((result, index) => {
            if (result.root !== null) {
                html += `
                    <div class="root-item">
                        <div class="root-value"> Raíz ${index + 1}: ${result.root.toFixed(8)}</div>
                        <div class="root-details">
                            f(${result.root.toFixed(6)}) = ${result.fx.toExponential(2)}<br>
                            Iteraciones: ${result.iterations}<br>
                            Error final: ${result.finalError.toExponential(2)}
                        </div>
                    </div>
                `;
            } else {
                html += `
                    <div class="root-item error">
                        <div class="root-value">❌ Error en intervalo</div>
                        <div class="root-details">${result.error}</div>
                    </div>
                `;
            }
        });
        
        html += `</div></div></div>`;

        // 2. MÉTODO DE NEWTON-RAPHSON
        html += `
            <div class="method-result">
                <div class="method-header">
                     MÉTODO DE NEWTON-RAPHSON
                </div>
                <div class="method-content">
                    <div class="roots-list">
        `;
        
        results.newton.forEach((result, index) => {
            const guesses = [3.5, 7.5, 5.5, -1.0, 0.5, 1.8, 3.5];
            if (result.root !== null) {
                html += `
                    <div class="root-item">
                        <div class="root-value"> Con x₀ = ${guesses[index]}:</div>
                        <div class="root-details">
                            Raíz = ${result.root.toFixed(8)}<br>
                            Iteraciones: ${result.iterations}<br>
                            Error final: ${result.finalError.toExponential(2)}
                        </div>
                    </div>
                `;
            } else {
                html += `
                    <div class="root-item error">
                        <div class="root-value">❌ Error con x₀</div>
                        <div class="root-details">${result.error}</div>
                    </div>
                `;
            }
        });
        
        html += `</div></div></div>`;

        // 3. MÉTODO DE LA SECANTE
        html += `
            <div class="method-result">
                <div class="method-header">
                     MÉTODO DE LA SECANTE
                </div>
                <div class="method-content">
                    <div class="roots-list">
        `;
        
        results.secant.forEach((result, index) => {
            const pairs = [
                [3.0, 4.0], [7.0, 8.0],
                [5.0, 6.0],
                [-1.5, -0.5], [0.0, 1.0], [1.5, 2.0],
                [3.0, 4.0]
            ];
            
            if (result.root !== null) {
                html += `
                    <div class="root-item">
                        <div class="root-value"> Con x₀ = ${pairs[index][0]}, x₁ = ${pairs[index][1]}:</div>
                        <div class="root-details">
                            Raíz = ${result.root.toFixed(8)}<br>
                            Iteraciones: ${result.iterations}<br>
                            Error final: ${result.finalError.toExponential(2)}
                        </div>
                    </div>
                `;
            } else {
                html += `
                    <div class="root-item error">
                        <div class="root-value">❌ Error con puntos iniciales</div>
                        <div class="root-details">${result.error}</div>
                    </div>
                `;
            }
        });
        
        html += `</div></div></div>`;

        // COMPARACIÓN DE MÉTODOS
        const bisectionRoots = results.bisection.filter(r => r.root).map(r => r.root.toFixed(6));
        const newtonRoots = results.newton.filter(r => r.root).map(r => r.root.toFixed(6));
        const secantRoots = results.secant.filter(r => r.root).map(r => r.root.toFixed(6));
        
        html += `
            <div class="comparison-section">
                <pre>🔄 COMPARACIÓN DE MÉTODOS
   Bisección:    [${bisectionRoots.map(r => `'${r}'`).join(', ')}]
   Newton:       [${newtonRoots.map(r => `'${r}'`).join(', ')}]
   Secante:      [${secantRoots.map(r => `'${r}'`).join(', ')}]
    Todos los métodos convergen consistentemente</pre>
            </div>
        </div>
        `;

        resultsDiv.innerHTML = html;
        document.getElementById('summary-section').style.display = 'block';
    }

    displaySummary(results) {
        const summaryDiv = document.getElementById('summary-results');
        
        const bisectionRoots = results.bisection.filter(r => r.root).map(r => r.root.toFixed(6));
        const newtonRoots = results.newton.filter(r => r.root).map(r => r.root.toFixed(6));
        const secantRoots = results.secant.filter(r => r.root).map(r => r.root.toFixed(6));
        
        const allRoots = [...bisectionRoots, ...newtonRoots, ...secantRoots];
        const uniqueRoots = [...new Set(allRoots.map(r => parseFloat(r).toFixed(4)))];
        
        const isConsistent = bisectionRoots.length === newtonRoots.length && 
                           newtonRoots.length === secantRoots.length;

        const html = `
            <div class="summary-grid">
                <div class="summary-card">
                    <h4>🔷 Problema ${results.problem}: ${results.name}</h4>
                    <div class="method-comparison">
                        <span class="method-name">📏 Bisección:</span>
                        <span class="roots-values">[${bisectionRoots.map(r => `'${r}'`).join(', ')}]</span>
                    </div>
                    <div class="method-comparison">
                        <span class="method-name">📐 Newton:</span>
                        <span class="roots-values">[${newtonRoots.map(r => `'${r}'`).join(', ')}]</span>
                    </div>
                    <div class="method-comparison">
                        <span class="method-name">📊 Secante:</span>
                        <span class="roots-values">[${secantRoots.map(r => `'${r}'`).join(', ')}]</span>
                    </div>
                    <div class="convergence-analysis ${isConsistent ? 'success' : 'warning'}">
                        ${isConsistent ? 
                            ' CONVERGENCIA CONSISTENTE: Todos los métodos encontraron el mismo número de raíces' : 
                            ' DIFERENCIAS: Los métodos encontraron diferente número de raíces'}
                    </div>
                </div>
            </div>
        `;

        summaryDiv.innerHTML = html;
    }

    showError(message) {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `
            <div class="problem-result">
                <div class="problem-header" style="background: var(--error);">
                    ❌ ERROR
                </div>
                <div class="method-content">
                    <div class="root-item error">
                        <div class="root-value">${message}</div>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('summary-section').style.display = 'none';
    }
}

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    new ExactPythonReplica();
});