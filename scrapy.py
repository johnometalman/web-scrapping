import scrapy
from scrapy.crawler import CrawlerProcess

def run():
    

    class Spider12(scrapy.Spider):
        name = 'spider12'
        allowed_domains = ['pagina12.com.ar']
        custom_settings = {'FEED_FORMAT': 'json', 
                        'FEED_URI': 'resultados.json', 
                        'DEPTH_LIMIT': 2}
        
        start_urls = ['https://www.pagina12.com.ar/secciones/el-pais',
                    'https://www.pagina12.com.ar/secciones/economia',
                    'https://www.pagina12.com.ar/secciones/sociedad',
                    'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                    'https://www.pagina12.com.ar/secciones/el-mundo',
                    'https://www.pagina12.com.ar/secciones/deportes',
                    'https://www.pagina12.com.ar/secciones/contratapa',
                    'https://www.pagina12.com.ar/secciones/audiovisuales']
    
        def parse(self, response):
            # Articulo Promocionado 
            
            nota_promocionada = response.xpath['//article[@class="top-content"]//h2/a/@href'].get()
            if nota_promocionada is not None:
                yield response.follow(nota_promocionada, callback = self.parse_nota)
                
            # listado de notas
            notas = response.xpath('//div[@class="articles-list"]//h4/a/@href').getall()
            for nota in notas:
                yield response.follow(nota, callback = self.parse_nota)
                
            #Link a la siguiente página
            next_page = response.xpath('//a[@class="next"]/@href')
            if next_page is not None:
                yield response.follow(next_page, callback = self.parse)
                
        def parse_nota(self, response):
            #Parseo de la nota
            titulo = response.xpath('//article[@class="article-full section"]//h1/text()').get()
            cuerpo = response.xpath('//div[@class="article-main-content article-text "]//text()').getall()
            if body is not None:
                body = ''.json(body)
                
            yield {'url': response.url, 
                'titulo': titulo, 
                'cuerpo': cuerpo}
    

    process = CrawlerProcess()
    process.crawl(Spider12)
    process.start()
            

if __name__ == '__main__':
    run()