import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import exp, sin, cos

class NumericalRootSolver:
    def __init__(self, function, derivative_func=None, tolerance=1e-6, max_iterations=100):
        self.function = function
        self.derivative_func = derivative_func
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    def binary_search_method(self, left_bound, right_bound):
        """Implementacion del algoritmo de division binaria"""
        f_left = self.function(left_bound)
        f_right = self.function(right_bound)
        
        if f_left * f_right >= 0:
            raise ValueError(f"f({left_bound}) = {f_left:.6f}, f({right_bound}) = {f_right:.6f}. No hay cambio de signo en el intervalo")
        
        iteration_data = []
        current_left = left_bound
        current_right = right_bound
        f_current_left = f_left
        
        for iteration_count in range(self.max_iterations):
            midpoint = (current_left + current_right) / 2
            f_midpoint = self.function(midpoint)
            current_error = abs(current_right - current_left) / 2
            
            iteration_data.append({
                'Paso_Iterativo': iteration_count + 1,
                'Limite_Inferior': current_left, 
                'Evaluacion_fa': f_current_left,
                'Limite_Superior': current_right, 
                'Evaluacion_fb': f_right,
                'Punto_Medio': midpoint, 
                'Evaluacion_fc': f_midpoint,
                'Error_Relativo': current_error
            })
            
            if abs(f_midpoint) < self.tolerance or current_error < self.tolerance:
                break
                
            if f_current_left * f_midpoint < 0:
                current_right, f_right = midpoint, f_midpoint
            else:
                current_left, f_current_left = midpoint, f_midpoint
                
        return midpoint, pd.DataFrame(iteration_data)
    
    def tangent_method(self, initial_guess):
        """Metodo de la tangente para aproximacion de raices"""
        if self.derivative_func is None:
            delta = 1e-7
            self.derivative_func = lambda x: (self.function(x + delta) - self.function(x - delta)) / (2 * delta)
        
        iteration_records = []
        current_x = initial_guess
        
        for step in range(self.max_iterations):
            function_value = self.function(current_x)
            derivative_value = self.derivative_func(current_x)
            
            if abs(derivative_value) < 1e-12:
                raise ValueError("La derivada es numericamente inestable")
            
            next_x = current_x - function_value / derivative_value
            approximation_error = abs(next_x - current_x)
            
            iteration_records.append({
                'Iteracion': step + 1,
                'Aproximacion_Actual': current_x, 
                'Valor_Funcion': function_value, 
                "Valor_Derivada": derivative_value,
                'Nueva_Aproximacion': next_x, 
                'Error_Absoluto': approximation_error
            })
            
            if abs(function_value) < self.tolerance or approximation_error < self.tolerance:
                break
                
            current_x = next_x
            
        return next_x, pd.DataFrame(iteration_records)
    
    def chord_method(self, first_guess, second_guess):
        """Algoritmo de la cuerda para encontrar raices"""
        iteration_history = []
        x_previous, x_current = first_guess, second_guess
        
        for iteration_number in range(self.max_iterations):
            f_previous = self.function(x_previous)
            f_current = self.function(x_current)
            
            if abs(f_current - f_previous) < 1e-12:
                raise ValueError("Las evaluaciones son numericamente identicas")
            
            x_next = x_current - f_current * (x_current - x_previous) / (f_current - f_previous)
            step_error = abs(x_next - x_current)
            
            iteration_history.append({
                'Iteracion': iteration_number + 1,
                'Punto_Anterior': x_previous, 
                'Punto_Actual': x_current,
                'Punto_Siguiente': x_next, 
                'Evaluacion_Funcion': f_current,
                'Error_Iteracion': step_error
            })
            
            if abs(f_current) < self.tolerance or step_error < self.tolerance:
                break
                
            x_previous, x_current = x_current, x_next
            
        return x_next, pd.DataFrame(iteration_history)

    def locate_sign_changes(self, start_point, end_point, sample_points=1000):
        """Identificar intervalos donde ocurren cambios de signo"""
        x_samples = np.linspace(start_point, end_point, sample_points)
        y_values = [self.function(x) for x in x_samples]
        
        sign_change_intervals = []
        for i in range(len(x_samples)-1):
            if y_values[i] * y_values[i+1] < 0:
                sign_change_intervals.append((x_samples[i], x_samples[i+1]))
        
        return sign_change_intervals

# Definicion de las ecuaciones del problema
def primera_ecuacion(x): 
    return x**3 - exp(0.8*x) - 20

def derivada_primera(x): 
    return 3*x**2 - 0.8*exp(0.8*x)

def segunda_ecuacion(x): 
    return 3*sin(0.5*x) - 0.5*x + 2

def derivada_segunda(x): 
    return 1.5*cos(0.5*x) - 0.5

def tercera_ecuacion(x): 
    return x**3 - x**2*exp(-0.5*x) - 3*x + 1

def derivada_tercera(x): 
    return 3*x**2 - (2*x*exp(-0.5*x) - 0.5*x**2*exp(-0.5*x)) - 3

def cuarta_ecuacion(x): 
    return cos(x)**2 - 0.5*x*exp(0.3*x) + 5

def derivada_cuarta(x): 
    return -2*cos(x)*sin(x) - 0.5*(exp(0.3*x) + 0.3*x*exp(0.3*x))

def examinar_comportamiento_funcion(funcion, nombre_ecuacion, rango_x):
    """Estudiar el comportamiento de la funcion en el intervalo dado"""
    valores_x = np.linspace(rango_x[0], rango_x[1], 1000)
    valores_y = [funcion(x) for x in valores_x]
    
    print(f"\nEXAMINANDO {nombre_ecuacion}:")
    print(f"   Rango de salida: [{min(valores_y):.4f}, {max(valores_y):.4f}]")
    
    intervalos_deteccion = []
    for i in range(len(valores_y)-1):
        if valores_y[i] * valores_y[i+1] < 0:
            aprox_raiz = valores_x[i] + (valores_x[i+1] - valores_x[i]) * abs(valores_y[i]) / (abs(valores_y[i]) + abs(valores_y[i+1]))
            intervalos_deteccion.append((valores_x[i], valores_x[i+1]))
            print(f"   [OK] Cambio de signo detectado cerca de x ~ {aprox_raiz:.4f} en [{valores_x[i]:.2f}, {valores_x[i+1]:.2f}]")
    
    if not intervalos_deteccion:
        print(f"   [ERROR] No se detectaron cambios de signo en [{rango_x[0]}, {rango_x[1]}]")
    
    return intervalos_deteccion

def resolver_problemas_numericos():
    """Funcion principal para resolver los cuatro problemas planteados"""
    
    problemas_configuracion = [
        {
            'nombre': "x^3 - e^(0.8x) = 20 entre x = 0 y x = 8",
            'funcion': primera_ecuacion, 
            'derivada': derivada_primera, 
            'dominio': (0, 8),
            'intervalos_biseccion': [(3.0, 4.0), (7.0, 8.0)],
            'semillas_newton': [3.5, 7.5],
            'pares_secante': [(3.0, 4.0), (7.0, 8.0)]
        },
        {
            'nombre': "3sin(0.5x) - 0.5x + 2 = 0", 
            'funcion': segunda_ecuacion, 
            'derivada': derivada_segunda, 
            'dominio': (0, 10),
            'intervalos_biseccion': [(5.0, 6.0)],
            'semillas_newton': [5.5],
            'pares_secante': [(5.0, 6.0)]
        },
        {
            'nombre': "x^3 - x^2e^(-0.5x) - 3x = -1",
            'funcion': tercera_ecuacion, 
            'derivada': derivada_tercera, 
            'dominio': (-2, 4),
            'intervalos_biseccion': [(-1.5, -0.5), (0.0, 1.0), (1.5, 2.0)],
            'semillas_newton': [-1.0, 0.5, 1.8],
            'pares_secante': [(-1.5, -0.5), (0.0, 1.0), (1.5, 2.0)]
        },
        {
            'nombre': "cos^2x - 0.5xe^(0.3x) + 5 = 0",
            'funcion': cuarta_ecuacion, 
            'derivada': derivada_cuarta, 
            'dominio': (0, 10),
            'intervalos_biseccion': [(3.0, 4.0)],
            'semillas_newton': [3.5],
            'pares_secante': [(3.0, 4.0)]
        }
    ]
    
    resultados_totales = []
    
    for indice, config in enumerate(problemas_configuracion, 1):
        print(f"\n{'='*80}")
        print(f"PROBLEMA {indice}: {config['nombre']}")
        print(f"{'='*80}")
        
        solver = NumericalRootSolver(config['funcion'], config['derivada'])
        intervalos_encontrados = examinar_comportamiento_funcion(config['funcion'], config['nombre'], config['dominio'])
        
        if intervalos_encontrados and len(intervalos_encontrados) > len(config['intervalos_biseccion']):
            print("   [INFO] Utilizando intervalos detectados automaticamente")
            config['intervalos_biseccion'] = intervalos_encontrados
            config['semillas_newton'] = [(a+b)/2 for a,b in intervalos_encontrados]
            config['pares_secante'] = intervalos_encontrados
        
        # Aplicacion del metodo de biseccion
        print(f"\n{'-'*40}")
        print("1. ALGORITMO DE DIVISION BINARIA")
        print(f"{'-'*40}")
        raices_biseccion = []
        for j, (a, b) in enumerate(config['intervalos_biseccion']):
            try:
                raiz, dataframe = solver.binary_search_method(a, b)
                raices_biseccion.append(raiz)
                print(f"   [OK] Raiz {j+1}: {raiz:.8f}")
                print(f"        Evaluacion: f({raiz:.6f}) = {config['funcion'](raiz):.2e}")
                print(f"        Pasos requeridos: {len(dataframe)}")
                print(f"        Error final: {dataframe['Error_Relativo'].iloc[-1]:.2e}")
            except Exception as error:
                print(f"   [ERROR] En intervalo [{a:.2f}, {b:.2f}]: {error}")
        
        # Aplicacion del metodo de Newton
        print(f"\n{'-'*40}")
        print("2. METODO DE LA TANGENTE")
        print(f"{'-'*40}")
        raices_newton = []
        for j, semilla in enumerate(config['semillas_newton']):
            try:
                raiz, dataframe = solver.tangent_method(semilla)
                raices_newton.append(raiz)
                print(f"   [OK] Con semilla x0 = {semilla}:")
                print(f"        Raiz = {raiz:.8f}")
                print(f"        Iteraciones: {len(dataframe)}")
                print(f"        Error final: {dataframe['Error_Absoluto'].iloc[-1]:.2e}")
            except Exception as error:
                print(f"   [ERROR] Con semilla x0 = {semilla}: {error}")
        
        # Aplicacion del metodo de la secante
        print(f"\n{'-'*40}")
        print("3. ALGORITMO DE LA CUERDA")
        print(f"{'-'*40}")
        raices_secante = []
        for j, (x0, x1) in enumerate(config['pares_secante']):
            try:
                raiz, dataframe = solver.chord_method(x0, x1)
                raices_secante.append(raiz)
                print(f"   [OK] Con puntos x0 = {x0}, x1 = {x1}:")
                print(f"        Raiz = {raiz:.8f}")
                print(f"        Iteraciones: {len(dataframe)}")
                print(f"        Error final: {dataframe['Error_Iteracion'].iloc[-1]:.2e}")
            except Exception as error:
                print(f"   [ERROR] Con x0 = {x0}, x1 = {x1}: {error}")
        
        resultados_totales.append({
            'problema': indice,
            'descripcion': config['nombre'],
            'raices_biseccion': raices_biseccion,
            'raices_newton': raices_newton,
            'raices_secante': raices_secante
        })
        
        # Analisis comparativo
        print(f"\n{'-'*40}")
        print("COMPARATIVA ENTRE METODOS")
        print(f"{'-'*40}")
        print(f"   Division Binaria: {[f'{r:.6f}' for r in raices_biseccion]}")
        print(f"   Metodo Tangente:  {[f'{r:.6f}' for r in raices_newton]}")
        print(f"   Algoritmo Cuerda: {[f'{r:.6f}' for r in raices_secante]}")
        
        todas_raices = raices_biseccion + raices_newton + raices_secante
        if todas_raices:
            raices_unicas = len(set([round(r, 4) for r in todas_raices]))
            raices_esperadas = len(config['intervalos_biseccion'])
            if raices_unicas == raices_esperadas:
                print(f"   [OK] Convergencia consistente en todos los metodos")
            else:
                print(f"   [AVISO] Discrepancia en el numero de raices identificadas")
        
        # Generar visualizacion
        generar_grafica_comparativa(config, raices_biseccion, raices_newton, raices_secante, indice)
    
    return resultados_totales

def generar_grafica_comparativa(configuracion, raices_bisec, raices_newt, raices_sec, num_problema):
    """Crear visualizacion grafica de la funcion y las raices encontradas"""
    x_valores = np.linspace(configuracion['dominio'][0], configuracion['dominio'][1], 400)
    y_valores = [configuracion['funcion'](x) for x in x_valores]
    
    plt.figure(figsize=(12, 8))
    plt.plot(x_valores, y_valores, 'b-', linewidth=2, label='f(x)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.grid(True, alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'PROBLEMA {num_problema}: {configuracion["nombre"]}')
    
    # Representar raices por metodo
    metodos_datos = [
        (raices_bisec, 'red', 'Division Binaria'),
        (raices_newt, 'green', 'Metodo Tangente'), 
        (raices_sec, 'purple', 'Algoritmo Cuerda')
    ]
    
    for raices, color, nombre_metodo in metodos_datos:
        for raiz in raices:
            plt.plot(raiz, configuracion['funcion'](raiz), 'o', 
                    color=color, markersize=8, 
                    label=f'{nombre_metodo}: {raiz:.4f}')
    
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'problema_{num_problema}_solucion.png', dpi=300, bbox_inches='tight')
    plt.show()

# Ejecucion principal
if __name__ == "__main__":
    print("ANALISIS NUMERICO DE RAICES - IMPLEMENTACION PERSONALIZADA")
    print("=" * 60)
    
    resultados = resolver_problemas_numericos()
    
    # Resumen ejecutivo
    print(f"\n{'='*80}")
    print("INFORME FINAL - COMPARATIVA DE METODOS NUMERICOS")
    print(f"{'='*80}")
    
    for resultado in resultados:
        print(f"\nEJERCICIO {resultado['problema']}: {resultado['descripcion']}")
        
        todas_las_raices = resultado['raices_biseccion'] + resultado['raices_newton'] + resultado['raices_secante']
        if todas_las_raices:
            print(f"   Division Binaria:  {[f'{r:.6f}' for r in resultado['raices_biseccion']]}")
            print(f"   Metodo Tangente:   {[f'{r:.6f}' for r in resultado['raices_newton']]}")
            print(f"   Algoritmo Cuerda:  {[f'{r:.6f}' for r in resultado['raices_secante']]}")
            
            raices_unicas = set([round(r, 4) for r in todas_las_raices])
            print(f"   Raices distintas identificadas: {len(raices_unicas)}")
            
            if len(resultado['raices_biseccion']) == len(resultado['raices_newton']) == len(resultado['raices_secante']):
                print("   [OK] CONVERGENCIA UNIFORME: Coincidencia en el numero de raices")
            else:
                print("   [AVISO] VARIACION: Diferente cantidad de raices por metodo")
        else:
            print("   [ERROR] No se identificaron raices reales con los metodos aplicados")

# Funcion adicional para analisis exhaustivo
def analisis_exhaustivo_intervalos():
    """Evaluacion detallada de intervalos para cada funcion"""
    print(f"\n{'#'*80}")
    print("EVALUACION EXHAUSTIVA DE INTERVALOS")
    print(f"{'#'*80}")
    
    funciones_analisis = [
        ("Ecuacion 1", primera_ecuacion, (0, 8)),
        ("Ecuacion 2", segunda_ecuacion, (0, 10)), 
        ("Ecuacion 3", tercera_ecuacion, (-2, 4)),
        ("Ecuacion 4", cuarta_ecuacion, (0, 10))
    ]
    
    for nombre, funcion, rango in funciones_analisis:
        print(f"\n{nombre} en [{rango[0]}, {rango[1]}]:")
        x_puntos = np.linspace(rango[0], rango[1], 20)
        for i in range(len(x_puntos)-1):
            a, b = x_puntos[i], x_puntos[i+1]
            fa, fb = funcion(a), funcion(b)
            if fa * fb < 0:
                print(f"   [OK] Intervalo viable: [{a:.2f}, {b:.2f}] - f({a:.2f})={fa:.2f}, f({b:.2f})={fb:.2f}")

# Ejecutar analisis complementario
# analisis_exhaustivo_intervalos()