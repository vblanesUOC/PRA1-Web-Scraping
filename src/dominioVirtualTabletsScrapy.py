from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

#Se crea el Item con las características deseadas para completarlas cuando se realice el WebScrapy de la web
class Producto(Item):
    modelo = Field()
    marca = Field()
    pulgadas = Field()
    calidad_imagen = Field()
    sistema_operativo = Field()
    peso = Field()
    precio_dominioVirtual= Field()

#Se define en el Spider como se desea que sea el proceso de Scrapy
class DominioVirtualSpider(CrawlSpider):
    name = 'dominioVirtualSpider'
    #Se asigna que los header referente al de desde donde se realiza la petición sea el de un navegador, ya que sino sale por defecto el de robot
    #al igual que se fija el número máximo de peticiones a realizar
    custom_settings = {
        # Necsario para hacer que cada vez llamamos desde un navegador (cambio de header)
        "DOWNLOADER_MIDDLEWARES": {
            # Para que no coja el de por defecto
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # Usar los recursos de la librería que se ha instalado para el cambio de user-agents
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
        # Se definen varios a partir de los cuales las peticiones irán rotando
        "USER_AGENTS": [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
            # chrome
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            # chrome
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',  # firefox
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
            # chrome
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
            # chrome
        ],
        #Se pone un número elevado al ser la categoría que más elementos tiene
        'CLOSESPIDER_PAGECOUNT': 100
    }

    #Se hace que cada petición se lance cada segundo, para evitar que los servidores nos relacionen como robots
    download_delay = 1

    # Acotar el espectro de búsqueda analizando las webs que se van a analizar, para evitra desvíos no deseados (no ir a publi por ejemplo)
    allowed_domains = ['dominiovirtual.es']

    #Se define la web por la que se empezará la búsqueda. En este caso, la sección de tablets de la web
    start_urls = ['https://www.dominiovirtual.es/20-tabletas']

    rules = (
        # Regla para hacer scrapy para las tablets
        Rule(
            # Fijándonos en el link de cada producto, se aprecia como siguen el patrón https://www.dominiovirtual.es/tabletas/idProducto/string/string.html
            # Por lo que transladando esta regla a código se traduce en un primer lugar en'/tabletas/\d+/', en donde, cada web con esta estructura, será parseada por
            # la función creada, ya que será en esta web desde donde se extraiga la info necesaria
            # Sin embargo, si solo se deja eso, se llegan a algunas webs terminadas en /contactanos que siguen la estructura del patron y que según el archivo robots.txt no se
            # pueden usar con webScrapy. Por tanto, se añade en la expresión regular .*\.html$ para que tan solo se vayan a las webs con estas estructuras

            LinkExtractor(
                allow=r'/tabletas/\d+/.*\.html$'
            ), follow=True, callback='parse_tableta'
        ),
        #No se mete paginación al no tener esta sección
    )
    #Mediante esta función se hará el parseo de cada Item. Será llamada como se ha visto, cuando se encuentre un item por medio de la primera Rule
    def parse_tableta(self, response):
        #Primero se crea el nuevo item
        item = ItemLoader(Producto(), response)
        # A continuación prestando atención a la estructura HTML de la web, y haciendo uso de XPATH, se asigna valor a cada una de las características deseadas
        #Por ejemplo, se puede apreciar como la marca se encuentran dentro del párrafo (p) con id product_mpn (p[@id="product_mpn"])
        #Una vez se está en la secció anterior, la propiedad estará dentro del span con la propiedas brand
        item.add_xpath('marca','//p[@id="product_mpn"]/span[@itemprop="brand"]/text()')
        #Para el modelo, se esocgerá de descripción (posteriormente se realizará limpieza) que se encuentra en el div con id short_description_content
        item.add_xpath('modelo','//div[@id="short_description_content"]/text()')
        # Para la mayoría del resto de categorías, se encuentran en diferentes td, en donde para su recolección, se presta atención al nombre que tiene este td en la web,
        # para buscar el inmediatamente posterior para obtener su valor (se tiene la estructura nombre categoría -valor)
        item.add_xpath('pulgadas',"//tr/td[text() = 'Diagonal de la pantalla:']/following-sibling::td[1]/text()")
        item.add_xpath('calidad_imagen',"//tr/td[text() = 'Tecnología de visualización:']/following-sibling::td[1]/text()")
        item.add_xpath('sistema_operativo',"//tr/td[text() = 'Sistema operativo instalado:']/following-sibling::td[1]/text()")
        item.add_xpath('peso',"//tr/td[text() = 'Peso:']/following-sibling::td[1]/text()")
        #Para el caso del precio, se encuentra un caso similar al del modelo y marca, en donde se aprecia que este aparece en un span cuyo id es "our_price_display"
        item.add_xpath('precio_dominioVirtual','//span[@id="our_price_display"]/text()')
        #Una vez extraídos todos los campos, se carga el item a la colección
        yield item.load_item()

#Para ejecutar
#scrapy runspider dominioVirtualTabletsScrapy.py -o tabletsDominioVirtual.csv -t csv