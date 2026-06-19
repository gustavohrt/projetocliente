from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, viewsets

from .forms import ClienteForm
from .models import Cliente
from .serializers import ClienteSerializer


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('lista_clientes')
    else:
        form = UserCreationForm()

    return render(request, 'registration/cadastrar_usuario.html', {'form': form})


@login_required
def lista_clientes(request):
    busca = request.GET.get('busca', '').strip()
    clientes_base = Cliente.objects.all()
    clientes = clientes_base

    if busca:
        clientes = clientes.filter(
            Q(nome__icontains=busca)
            | Q(cpf__icontains=busca)
            | Q(cnpj__icontains=busca)
            | Q(inscricao_estadual__icontains=busca)
            | Q(telefone__icontains=busca)
            | Q(rua__icontains=busca)
            | Q(bairro__icontains=busca)
            | Q(cep__icontains=busca)
            | Q(estado__icontains=busca)
        )

    return render(
        request,
        'clientes/lista_clientes.html',
        {
            'clientes': clientes,
            'busca': busca,
            'total_clientes': clientes_base.count(),
            'total_ativos': clientes_base.filter(ativo=True).count(),
            'total_inativos': clientes_base.filter(ativo=False).count(),
        },
    )


@login_required
def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.criado_por = request.user
            cliente.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/form_cliente.html', {'form': form, 'titulo': 'Novo cliente'})


@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/form_cliente.html', {'form': form, 'titulo': 'Editar cliente'})


@login_required
def ver_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'clientes/ver_cliente.html', {'cliente': cliente})


@login_required
def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')

    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': cliente})


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cliente.objects.all()

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
