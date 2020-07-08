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
        )),
    ('mssql_3', (
        'murom mytishchi naberezhnye nakhodka nalchik naro nazran neftekamsk nefteyugansk neryungri nevinnomyssk '
        'nizhnekamsk nizhnevartovsk noginsk norilsk novoaltaysk novocheboksarsk novocherkassk novokuybyshevsk '
        'novokuznetsk novomoskovsk novorossiysk novoshakhtinsk novosibirsk novotroitsk novouralsk novy noyabrsk '
        'nyagan obninsk odintsovo oktyabrsky omsk orekhovo orenburg orsk oryol ozyorsk pavlovo pavlovsky penza perm '
        'pervouralsk petropavlovsk petrozavodsk podolsk polevskoy prokhladny prokopyevsk pskov '
        )),
    ('mssql_4', (
        'pushkino pyatigorsk ramenskoye reutov revda rossosh rostov rubtsovsk ryazan rybinsk rzhev saint salavat '
        'salekhard salsk samara saransk sarapul saratov sarov sergiyev serov serpukhov sertolovo severodvinsk '
        'severomorsk seversk shadrinsk shakhty shali shchyokino shchyolkovo shuya sibay slavyansk smolensk snezhinsk '
        'sochi solikamsk solnechnogorsk sosnovy stary stavropol sterlitamak stupino sunzha surgut svobodny syktyvkar '
        'syzran '
        ))])]
