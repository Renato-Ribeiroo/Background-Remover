# 🖼️ Removedor de Fundo de Imagem

![Removedor de Fundo](https://img.shields.io/badge/Removerdor-Fundo-brightgreen)

Aplicação de interface gráfica (GUI) desenvolvida com **PySide6** que permite ao usuário remover facilmente o fundo de imagens com poucos cliques. Utiliza a biblioteca `rembg`, baseada em deep learning, para fazer a remoção automática do fundo.

---

## 🚀 Funcionalidades

- 📂 Seleção de imagens nos formatos `.png`, `.jpg` ou `.jpeg`
- 🤖 Remoção automática do fundo com base em IA
- 👁️ Pré-visualização da imagem sem fundo
- 💾 Salvamento da imagem processada no formato `.png`
- 📊 Barra de progresso para indicar o processamento

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [PySide6](https://doc.qt.io/qtforpython/)
- [Pillow (PIL)](https://python-pillow.org/)
- [rembg](https://github.com/danielgatis/rembg)

---

## 💻 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/removedor-fundo-imagem.git
cd removedor-fundo-imagem
```

### 2. Crie e ative um ambiente virtual (recomendado)
```bash
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o aplicativo
```bash
python main.py
```


