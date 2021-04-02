from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Producto(Item):
    modelo = Field()
    marca = Field()
    pulgadas = Field()
    calidad_imagen = Field()
    sistema_operativo = Field()
    peso = Field()
    precio= Field()


class DominioVirtualSpider(CrawlSpider):
    name = 'dominioVirtualSpider'
    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        'CLOSESPIDER_PAGECOUNT': 200
    }

    download_delay = 1

    allowed_domains = ['dominiovirtual.es'] #Acotar el espectro de búsqueda (no ir a publi por ejemplo)

    start_urls = ['https://www.dominiovirtual.es/13-ordenadores-portatiles']

    rules = (
        # Ordenadores portátiles
        Rule(
            LinkExtractor(
                #allow=r'/\w+/\d+/.*'
                allow=r'/ordenadores-portatiles/\d+/'
            ), follow=True, callback='parse_portatil'
        ),
        # Parse any
        #Rule(
        #    LinkExtractor(
        #       allow=r'/\w+/\d+/.*'
        #    ), follow=True, callback='parse_any'
        #),
        # Paginación
        Rule(
            LinkExtractor(
                allow=r'&p=\d+'
            ), follow=True
        )
    )

    def parse_portatil(self, response):
        item = ItemLoader(Producto(), response)
        item.add_xpath('modelo','//p[@id="product_mpn"]/span[@itemprop="mpn"]/text()')
        item.add_xpath('marca','//p[@id="product_mpn"]/span[@itemprop="brand"]/text()')
        item.add_xpath('pulgadas',"//tr/td[text() = 'Tamaño:']/following-sibling::td[1]/text()")
        item.add_xpath('calidad_imagen',"//tr/td[text() = 'Tipo HD:']/following-sibling::td[1]/text()")
        item.add_xpath('sistema_operativo',"//tr/td[text() = 'Sistema operativo instalado:']/following-sibling::td[1]/text()")
        item.add_xpath('peso',"//tr/td[text() = 'Peso:']/following-sibling::td[1]/text()")
        item.add_xpath('precio','//span[@id="our_price_display"]/text()')
        yield item.load_item()

