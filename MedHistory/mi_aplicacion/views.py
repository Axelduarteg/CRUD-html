# mi_aplicacion/views.py
from django.shortcuts import render, redirect
import pandas as pd
from django.conf import settings

def index(request):
    return render(request, 'mi_aplicacion/index.html')

csv_file_path = settings.BASE_DIR / 'data.csv'

try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    df = pd.DataFrame(columns=['ID', 'Nombre', 'Apellido', 'Fecha_Nacimiento', 'Dirección', 'Teléfono', 'Alergias'])

def create_view(request):
    if request.method == 'POST':
        Nombre = request.POST.get('Nombre')
        Apellido = request.POST.get('Apellido')
        Fecha_Nacimiento = request.POST.get('Fecha_Nacimiento')
        Dirección = request.POST.get('Dirección')
        Teléfono = request.POST.get('Teléfono')
        Alergias = request.POST.get('Alergias')

        nueva_fila = {
            'ID': len(df) + 1,
            'Nombre': Nombre,
            'Apellido': Apellido,
            'Fecha_Nacimiento': Fecha_Nacimiento,
            'Dirección': Dirección,
            'Teléfono': Teléfono,
            'Alergias': Alergias
        }
        df.loc[len(df)] = nueva_fila
        df.to_csv(csv_file_path, index=False)
        return redirect('detalle', id=nueva_fila['ID'])

    return render(request, 'mi_aplicacion/formulario.html', {'registro': None})

def buscar(request):
    query = request.GET.get('query', '')
    resultados = []

    if query:
        resultados = df[(df['ID'].astype(str).str.contains(query)) | 
                        (df['Nombre'].str.contains(query, case=False)) | 
                        (df['Apellido'].str.contains(query, case=False))]
        resultados = resultados.to_dict(orient='records')

    return render(request, 'mi_aplicacion/busqueda.html', {'resultados': resultados})

def detalle(request, id):
    registro = df[df['ID'] == id].to_dict(orient='records')
    if registro:
        registro = registro[0]
    return render(request, 'mi_aplicacion/detalle.html', {'registro': registro})

def actualizar(request, id):
    if request.method == 'POST':
        ID = id
        Nombre = request.POST.get('Nombre')
        Apellido = request.POST.get('Apellido')
        Fecha_Nacimiento = request.POST.get('Fecha_Nacimiento')
        Dirección = request.POST.get('Dirección')
        Teléfono = request.POST.get('Teléfono')
        Alergias = request.POST.get('Alergias')

        df.loc[df['ID'] == ID, 'Nombre'] = Nombre
        df.loc[df['ID'] == ID, 'Apellido'] = Apellido
        df.loc[df['ID'] == ID, 'Fecha_Nacimiento'] = Fecha_Nacimiento
        df.loc[df['ID'] == ID, 'Dirección'] = Dirección
        df.loc[df['ID'] == ID, 'Teléfono'] = Teléfono
        df.loc[df['ID'] == ID, 'Alergias'] = Alergias
        df.to_csv(csv_file_path, index=False)
        return redirect('detalle', id=ID)

    registro = df[df['ID'] == id].to_dict(orient='records')[0]
    return render(request, 'mi_aplicacion/formulario.html', {'registro': registro})

def eliminar(request, id):
    global df
    if request.method == 'POST':
        df = df[df['ID'] != id]
        df.to_csv(csv_file_path, index=False)
        return redirect('buscar')

    registro = df[df['ID'] == id].to_dict(orient='records')[0]
    return render(request, 'mi_aplicacion/eliminar.html', {'registro': registro})


