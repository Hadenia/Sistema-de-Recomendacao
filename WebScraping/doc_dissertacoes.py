#Desenvolvido por Hadênia Rodrigues
#Baseado em https://docs.scrapy.org/en/latest/intro/tutorial.html

#Captura de dados de dissertações de mestrado da PPGEE em repositorio UFRN

import scrapy

class DissertacaoSpider(scrapy.Spider):
    name = "doc_dissertacoes"
    start_urls = ["https://repositorio.ufrn.br/handle/123456789/12008"]

    def parse(self, response):
        page_links = response.css("strong a::attr(href)")
        yield from response.follow_all(page_links, self.parse_dissertacao)

        pagination_links = response.css(".prev-next-links a")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_dissertacao(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()         
        
        yield{
            'titulo': extract_with_css('td.metadataFieldValue.dc_title::text'),
            'autor': extract_with_css('a.author::text'),
            'link': extract_with_css('.dc_identifier_uri a::text'),
            'abstract': extract_with_css('td.metadataFieldValue.dc_description_abstract::text'),
            'resumo': extract_with_css('td.metadataFieldValue.dc_description_resumo::text')
        }

#Compilar
# cd tutorial
# scrapy crawl doc_dissertacoes -O doc_dissertacoes.csv