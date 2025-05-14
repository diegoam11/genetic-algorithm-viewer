from django.shortcuts import render, redirect
from .genetic_algorithm import GeneticAlgorithm, get_function_name

def inicio(request):
    return render(request, 'genetic_algorithms/inicio.html')

def ejecutar_algoritmo(request):
    if request.method == 'POST':
        # Obtener parámetros del formulario
        function_type = request.POST.get('function_type', 'simple_quadratic')
        population_size = int(request.POST.get('population_size', 50))
        num_generations = int(request.POST.get('num_generations', 50))
        mutation_rate = float(request.POST.get('mutation_rate', 10))
        crossover_rate = float(request.POST.get('crossover_rate', 70))
        min_value = float(request.POST.get('min_value', -10))
        max_value = float(request.POST.get('max_value', 10))
        
        # Crear y ejecutar el algoritmo genético
        ga = GeneticAlgorithm(
            population_size=population_size,
            num_generations=num_generations,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,
            min_value=min_value,
            max_value=max_value,
            function_type=function_type
        )
        
        results = ga.evolve()
        
        # Preparar datos para la plantilla
        context = {
            'function_type': function_type,
            'function_name': get_function_name(function_type),
            'population_size': population_size,
            'num_generations': num_generations,
            'mutation_rate': mutation_rate,
            'crossover_rate': crossover_rate,
            'min_value': min_value,
            'max_value': max_value,
            'best_solution': results['best_individual'],
            'best_fitness': results['best_fitness'],
            'best_generation': results['best_generation'],
            'generation_stats': results['generation_stats'],
        }
        
        return render(request, 'genetic_algorithms/resultado.html', context)
    
    # Si no es POST, redirigir al inicio
    return redirect('inicio')

def servicios(request):
    return render(request, 'genetic_algorithms/servicios.html')

def contacto(request):
    return render(request, 'genetic_algorithms/contacto.html')