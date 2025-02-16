import discord
from discord.ext import commands

# Configurações iniciais do bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Preços fixos
PRECO_ARMA = 1000
PRECO_MUNICAO = 30

# Comando para iniciar o processo de seleção de profissão
@bot.command()
async def comprar(ctx: commands.Context):
    # Cria um menu de seleção de profissões
    menu_selecao = discord.ui.Select(placeholder='🛠️Escolha sua profissão🛠️')
    opcoes = [
        discord.SelectOption(label='Polícial', value='Polícial'),
        discord.SelectOption(label='Médico', value='Médico'),
        discord.SelectOption(label='Engenheiro', value='Engenheiro'),
        discord.SelectOption(label='Professor', value='Professor'),
        discord.SelectOption(label='Advogado', value='Advogado')
    ]
    menu_selecao.options = opcoes

    # Cria uma view para o menu de seleção
    view = discord.ui.View()
    view.add_item(menu_selecao)

    # Envia a mensagem com o menu de seleção
    await ctx.send("🛠️Selecione a profissão abaixo para iniciar a venda!🛠️", view=view)

    # Função para lidar com a seleção da profissão
    async def select_callback(interaction: discord.Interaction):
        profissao = menu_selecao.values[0]
        await interaction.response.send_modal(RegistroModal(profissao))

    menu_selecao.callback = select_callback

# Modal para coletar as informações de compra
class RegistroModal(discord.ui.Modal):
    def __init__(self, profissao):
        super().__init__(title='💰 Informações de Compra 💰')
        self.profissao = profissao

    nome = discord.ui.TextInput(label='🪪 NOME', placeholder='Digite o Nome')
    id_passaporte = discord.ui.TextInput(label='🆔 ID/PASSAPORTE', placeholder='Digite o ID/Passaporte')
    quantidade_armas = discord.ui.TextInput(label='🔫 QUANTIDADE DE ARMAS', placeholder='Digite a quantidade de armas')
    quantidade_municoes = discord.ui.TextInput(label='🔫 QUANTIDADE DE MUNIÇÕES', placeholder='Digite a quantidade de munições')

    async def on_submit(self, interaction: discord.Interaction):
        # Calcula o preço total das armas e munições
        try:
            qtd_armas = int(self.quantidade_armas.value)
            qtd_municoes = int(self.quantidade_municoes.value)
        except ValueError:
            await interaction.response.send_message("Quantidade de armas ou munições inválida!", ephemeral=True)
            return

        preco_total_armas = qtd_armas * PRECO_ARMA
        preco_total_municoes = qtd_municoes * PRECO_MUNICAO
        preco_total = preco_total_armas + preco_total_municoes

        # Cria a mensagem de resumo
        mensagem = (
            f"**Resumo da Compra**\n"
            f"🪪 Nome: {self.nome.value}\n"
            f"🆔 ID/Passaporte: {self.id_passaporte.value}\n"
            f"👨‍💼 Profissão: {self.profissao}\n"
            f"🔫 Quantidade de Armas: {qtd_armas} (R$ {preco_total_armas:.2f})\n"
            f"🔫 Quantidade de Munições: {qtd_municoes} (R$ {preco_total_municoes:.2f})\n"
            f"💵 **Preço Total: R$ {preco_total:.2f}**"
        )

        # Envia a mensagem privada para o usuário
        await interaction.user.send(mensagem)
        await interaction.response.send_message("✅Compra registrada com sucesso!✅\nVerifique sua mensagem privada.", ephemeral=True)

# Evento para quando o bot estiver pronto
@bot.event
async def on_ready():
    print(f"Bot {bot.user} está pronto!")

# Inicia o bot
bot.run("token-bot")