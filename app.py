from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# URL da página do FII
url = 'https://statusinvest.com.br/fundos-imobiliarios/gare11'

# Função para fazer web scraping e obter a cotação do FII
def get_fii_price():
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Exibir a estrutura da página para depuração
        #print(soup.prettify())
        price_element = soup.find('strong', class_='value')
        if price_element:
            return price_element.text.strip()
    else:
        print(f"Erro ao acessar a página: {response.status_code}")
    return None

# Rota principal
@app.route('/')
def index():
    # Obter a cotação do FII via web scraping
    price = get_fii_price()

    if price:
        return render_template('index.html', price=price, url=url)
    else:
        return render_template('index.html', price="Cotação não encontrada", url=url)

if __name__ == '__main__':
    app.run(debug=True)
