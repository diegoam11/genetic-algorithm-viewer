import numpy as np
import random
import math

class GeneticAlgorithm:
    """Implementación básica de un algoritmo genético."""
    
    def __init__(self, population_size, num_generations, mutation_rate, crossover_rate, 
                 min_value, max_value, dimensions=1, function_type='simple_quadratic'):
        """
        Inicializa el algoritmo genético.
        
        Args:
            population_size: Tamaño de la población
            num_generations: Número de generaciones a evolucionar
            mutation_rate: Tasa de mutación (0-100)
            crossover_rate: Tasa de cruce (0-100)
            min_value: Valor mínimo para los genes
            max_value: Valor máximo para los genes
            dimensions: Número de dimensiones (variables) del problema
            function_type: Tipo de función de aptitud a utilizar
        """
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate / 100.0  # Convertir de porcentaje a fracción
        self.crossover_rate = crossover_rate / 100.0  # Convertir de porcentaje a fracción
        self.min_value = min_value
        self.max_value = max_value
        self.dimensions = dimensions
        self.function_type = function_type
        
        # Determinar dimensiones según la función
        if function_type == 'simple_quadratic':
            self.dimensions = 1
        elif function_type in ['complex', 'rastrigin']:
            self.dimensions = 2
        
        # Inicializar población aleatoria
        self.population = self._initialize_population()
        
        # Variables para seguimiento
        self.best_individual = None
        self.best_fitness = float('-inf')
        self.best_generation = 0
        self.generation_stats = []
    
    def _initialize_population(self):
        """Inicializa la población con valores aleatorios en el rango especificado."""
        population = []
        for _ in range(self.population_size):
            individual = [random.uniform(self.min_value, self.max_value) for _ in range(self.dimensions)]
            population.append(individual)
        return population
    
    def _fitness_function(self, individual):
        """Calcula el valor de aptitud para un individuo según la función seleccionada."""
        if self.function_type == 'simple_quadratic':
            # f(x) = -(x-5)² + 10 (queremos maximizar, por lo que usamos negativo)
            x = individual[0]
            return -(x - 5)**2 + 10
        
        elif self.function_type == 'complex':
            # f(x,y) = sin(x) + cos(y)
            x, y = individual
            return math.sin(x) + math.cos(y)
        
        elif self.function_type == 'rastrigin':
            # Función de Rastrigin (problema difícil con múltiples máximos locales)
            # Invertimos para maximizar en lugar de minimizar
            A = 10
            result = -A * self.dimensions
            for x in individual:
                result -= (x**2 - A * math.cos(2 * math.pi * x))
            return result  # Valor negativo - convertimos a problema de maximización
        
        # Valor por defecto
        return 0
    
    def _select_parents(self, fitnesses):
        """Selecciona padres usando selección por rueda de ruleta."""
        # Ajustar las aptitudes para manejar valores negativos
        min_fitness = min(fitnesses)
        adjusted_fitnesses = [f - min_fitness + 1e-6 for f in fitnesses]  # Asegurar valores positivos
        total_fitness = sum(adjusted_fitnesses)
        
        if total_fitness <= 0:
            # Si todos tienen aptitud cero o hay algún problema, selección uniforme
            return random.sample(range(len(self.population)), 2)
        
        # Normalizar las aptitudes para que sumen 1
        selection_probs = [f/total_fitness for f in adjusted_fitnesses]
        
        # Verificar que las probabilidades son válidas
        if any(p < 0 for p in selection_probs) or abs(sum(selection_probs) - 1.0) > 1e-10:
            # Si hay algún problema, usar selección uniforme
            return random.sample(range(len(self.population)), 2)
        
        try:
            # Seleccionar dos padres
            selected_indices = np.random.choice(
                len(self.population), 
                size=2, 
                replace=False, 
                p=selection_probs
            )
            return selected_indices
        except ValueError:
            # Si hay algún error, usar selección uniforme
            return random.sample(range(len(self.population)), 2)
    
    def _crossover(self, parent1, parent2):
        """Realiza cruce de un punto entre dos padres."""
        if random.random() > self.crossover_rate:
            return parent1[:], parent2[:]
        
        if self.dimensions == 1:
            # Para problemas de una dimensión, cruzamos aleatoriamente
            if random.random() < 0.5:
                return parent1[:], parent2[:]
            else:
                return parent2[:], parent1[:]
        
        # Para múltiples dimensiones, cruce de un punto
        crossover_point = random.randint(1, self.dimensions - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return child1, child2
    
    def _mutate(self, individual):
        """Aplica mutación a un individuo."""
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                # Aplicar mutación gaussiana
                mutation = random.gauss(0, (self.max_value - self.min_value) / 10)
                individual[i] += mutation
                
                # Asegurar que se mantiene en el rango
                individual[i] = max(self.min_value, min(individual[i], self.max_value))
        
        return individual
    
    def evolve(self):
        """Ejecuta el algoritmo genético y devuelve los resultados."""
        for generation in range(self.num_generations):
            # Evaluar la aptitud de toda la población
            fitnesses = [self._fitness_function(ind) for ind in self.population]
            
            # Guardar estadísticas de generación
            avg_fitness = sum(fitnesses) / len(fitnesses) if fitnesses else 0
            
            if fitnesses:
                current_best_idx = fitnesses.index(max(fitnesses))
                current_best_fitness = fitnesses[current_best_idx]
                current_best_individual = self.population[current_best_idx][:]
            else:
                current_best_fitness = 0
                current_best_individual = self.population[0][:] if self.population else []
            
            self.generation_stats.append({
                'generation': generation + 1,
                'best_fitness': current_best_fitness,
                'avg_fitness': avg_fitness
            })
            
            # Actualizar el mejor global si es necesario
            if current_best_fitness > self.best_fitness:
                self.best_fitness = current_best_fitness
                self.best_individual = current_best_individual
                self.best_generation = generation + 1
            
            # Crear nueva población
            new_population = []
            
            # Elitismo: conservar al mejor individuo
            if current_best_individual:
                new_population.append(current_best_individual)
            
            # Generar resto de la población
            while len(new_population) < self.population_size:
                # Seleccionar padres
                parent_indices = self._select_parents(fitnesses)
                parent1 = self.population[parent_indices[0]]
                parent2 = self.population[parent_indices[1]]
                
                # Cruzar
                child1, child2 = self._crossover(parent1, parent2)
                
                # Mutar y añadir a la nueva población
                new_population.append(self._mutate(child1))
                if len(new_population) < self.population_size:
                    new_population.append(self._mutate(child2))
            
            # Reemplazar la antigua población con la nueva
            self.population = new_population
        
        # Si no se encontró una solución (esto no debería ocurrir), inicializar valores
        if self.best_individual is None and self.population:
            self.best_individual = self.population[0]
            self.best_fitness = self._fitness_function(self.best_individual)
            self.best_generation = self.num_generations
        
        # Retornar resultados
        return {
            'best_individual': self.best_individual or [],
            'best_fitness': self.best_fitness,
            'best_generation': self.best_generation,
            'generation_stats': self.generation_stats
        }


def get_function_name(function_type):
    """Devuelve el nombre legible de la función seleccionada."""
    if function_type == 'simple_quadratic':
        return "f(x) = -(x-5)² + 10 (Función cuadrática simple)"
    elif function_type == 'complex':
        return "f(x,y) = sin(x) + cos(y) (Función trigonométrica 2D)"
    elif function_type == 'rastrigin':
        return "Función de Rastrigin (Múltiples máximos locales)"
    return "Función desconocida"