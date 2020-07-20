from collections import namedtuple
from itertools import product, chain

Datasource = namedtuple('Datasource', 'conn_id schema')


sql_server_ds = [Datasource(conn_id, city) for conn_id, city in chain.from_iterable(
    product([conn_id], cities.split()) for conn_id, cities in [
    ('mssql_0', (
        'abakan achinsk aleksin alexandrov almetyevsk anapa angarsk anzhero apatity arkhangelsk armavir arsenyev '
        'artyom arzamas asbest astrakhan azov balakovo balashikha balashov barnaul bataysk belebey belgorod belogorsk '
        'belorechensk beloretsk belovo berdsk berezniki beryozovsky birobidzhan biysk blagoveshchensk bor borisoglebsk '
        'bratsk bryansk budyonnovsk bugulma buynaksk buzuluk chapayevsk chaykovsky cheboksary chekhov chelyabinsk '
        'cheremkhovo cherepovets cherkessk'
        )),
    ('mssql_1', (
        'chernogorsk chistopol chita derbent dimitrovgrad dmitrov dolgoprudny domodedovo donskoy dubna dzerzhinsk '
        'dzerzhinsky elektrostal elista engels fryazino gatchina gelendzhik georgiyevsk glazov gorno grozny gubkin '
        'gudermes gukovo gus irkutsk ishim ishimbay iskitim ivanovo ivanteyevka izberbash izhevsk kaliningrad kaluga '
        'kamyshin kansk kaspiysk kazan kemerovo khabarovsk khanty khasavyurt khimki kineshma kirishi kirov kirovo '
        'kiselyovsk'
        )),
    ('mssql_2', (
        'kislovodsk klin klintsy kogalym kolomna komsomolsk kopeysk korolyov kostroma kotlas kovrov krasnodar '
        'krasnogorsk krasnokamensk krasnokamsk krasnoturyinsk krasnoyarsk kropotkin krymsk kstovo kumertau kungur '
        'kurgan kursk kuznetsk kyzyl labinsk leninogorsk leninsk lesosibirsk lipetsk liski lobnya lysva lytkarino '
        'lyubertsy magadan magnitogorsk makhachkala maykop meleuz mezhdurechensk miass michurinsk mikhaylovka '
        'mikhaylovsk mineralnye minusinsk moscow murmansk '
        ))])]
