import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import google.generativeai as genai

# Configurar a chave da API do Google
GOOGLE_API_KEY = 'COLE_SUA_API_KEY_AQUI'
genai.configure(api_key=GOOGLE_API_KEY)

# Configurações do modelo
generation_config = {
    "candidate_count": 1,
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = {
    'HATE': 'BLOCK_NONE',
    'HARASSMENT': 'BLOCK_NONE',
    'SEXUAL': 'BLOCK_NONE',
    'DANGEROUS': 'BLOCK_MEDIUM_AND_ABOVE'
}

# Inicialização do modelo
model = genai.GenerativeModel(
    model_name='gemini-1.0-pro',
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Funções para exibir uma instrução dentro do campo 
def on_entry_click(event):
    if app.prompt_entry.get() == "Digite um comando aqui...":
        app.prompt_entry.delete(0, tk.END)  # Remove o texto de instrução ao clicar

def on_focus_out(event):
    if app.prompt_entry.get() == "":
        app.prompt_entry.insert(0, "Digite um comando aqui...")  # Restaura o texto de instrução se o campo estiver vazio

# Função de resposta 
def show_response(prompt_entry, response_text):  
    response_text.delete(1.0, tk.END)  

    prompt = prompt_entry.get().strip()  

    if prompt == "Digite sua pergunta aqui...":  
        messagebox.showwarning("Aviso", "Por favor, insira uma pergunta.")  
        return  

    if prompt.lower() == "digite o comando":
        prompt_entry.delete(0, tk.END)  # Limpar o campo de entrada
        return

    response = model.start_chat(history=[]).send_message(prompt)  
    
    # Iterando sobre as mensagens da resposta
    for message in response:
        # Substituindo "*" por "•" no texto da mensagem
        formatted_message = message.text.replace('**', ' ')
        # Adicionando a mensagem formatada na response_text
        response_text.insert(tk.END, formatted_message)
        response_text.insert(tk.END, "\n")
    
class ChatInterface:
    def __init__(self, master):
        self.master = master
        master.title("CodeSensei Chatbot")

        # Definindo a cor de fundo da janela
        self.master.configure(bg='#162228')  
        
        # Definindo o tamanho da janela
        master.geometry("900x800")  # Largura x Altura

        # Carregar imagem de logo
        self.logo_image = Image.open("img/logo2.png")
        self.logo_image.thumbnail((150, 150))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(master, image=self.logo_photo, borderwidth=0)
        self.logo_label.image = self.logo_photo
        self.logo_label.pack()
        
        # Estilo de fonte e tamanho 
        custom_font = ("Calibri", 12)
        custom_fonte = ("Calibri", 10)
        
        # Exibindo Mensagem Inicial
        self.static_text = tk.Label(master, text="Olá, eu sou o CodeSensei, seu mentor de programação.",  bg='#162228', fg='white', font=custom_font)
        self.static_text.pack() 
        
        self.static_text = tk.Label(master, text="Selecione o seu nível de experiência:",  bg='#162228', fg='white', font=custom_font)
        self.static_text.pack() 
        
        # Criando um frame para os botões
        self.button_frame = tk.Frame(master, bg='#162228')
        self.button_frame.pack(pady=20)

        # Botões de nível de experiência
        self.beginner_button = tk.Button(self.button_frame, text="Iniciante", command=self.show_beginner_message, bg='#427989', fg='white', relief=tk.FLAT)
        self.beginner_button.pack(side=tk.LEFT, padx=5)

        self.intermediate_button = tk.Button(self.button_frame, text="Intermediário", command=self.show_intermediate_message, bg='#427989', fg='white', relief=tk.FLAT)
        self.intermediate_button.pack(side=tk.LEFT, padx=5)

        self.advanced_button = tk.Button(self.button_frame, text="Avançado", command=self.show_advanced_message, bg='#427989', fg='white', relief=tk.FLAT)
        self.advanced_button.pack(side=tk.LEFT, padx=5)

        self.output_text = tk.Text(master, height= 4, width=80, bg='#162228', borderwidth=0, fg='white', font=custom_font)
        self.output_text.pack()
        
        # Frame para botão e campo 
        frame = tk.Frame(master,  bg='#162228')
        frame.pack()

        # Campo para digitar o comando/prompt 
        self.prompt_entry = tk.Entry(frame, width=60, bg='#162228', borderwidth=1, fg='#D9D9D9', font=custom_font)  
        self.prompt_entry.insert(0, "Digite um comando aqui...")
        self.prompt_entry.bind("<FocusIn>", on_entry_click)
        self.prompt_entry.bind("<FocusOut>", on_focus_out)
        self.prompt_entry.pack(side="left")   
        
        # Botão enviar
        send_button = tk.Button(frame, text="Enviar", width=15, relief=tk.FLAT, font=custom_fonte,  bg='#427989', fg='white', command=lambda: show_response(self.prompt_entry, response_text))  
        send_button.pack(side="left", padx=5)  

        # Resposta da IA 
    
        response_text = tk.Text(master, height=30, width=100, bg='#162228', borderwidth=1, fg='white', font=("Calibri", 12))
        response_text.pack(pady=5)  # Espaçamento vertical entre o widget e os demais elementos
        response_text.tag_configure("bold", font=("Calibri", 12, "bold"))
        

    
    # Inicializando 
    def start_chat(self):
        self.entry.pack_forget()
        self.submit_button.pack_forget()
        self.prompt_label.pack()
        self.prompt_entry.pack()
        self.send_button.pack()
    
    # Funções para exibir as mensagens correspondentes aos botões de níveis de experiência 
    def show_beginner_message(self):
        self.output_text.insert(tk.END, "\n Você selecionou o nível iniciante. Para começar, recomendo que você aprenda os fundamentos da programação, como variáveis, operadores e estruturas de controle.\n")

    def show_intermediate_message(self):
        self.output_text.insert(tk.END, "\n Você selecionou o nível intermediário. Neste nível, é importante aprofundar seus conhecimentos em estruturas de dados, funções e classes.\n\n")

    def show_advanced_message(self):
        self.output_text.insert(tk.END, "\n Você selecionou o nível avançado. Neste estágio, você deve se concentrar em tópicos avançados, como programação concorrente, design patterns e algoritmos complexos.\n\n")

# Encerrando 
root = tk.Tk()
app = ChatInterface(root)
root.mainloop()
