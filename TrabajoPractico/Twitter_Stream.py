import sys
import time
if __name__ == '__main__':

    from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, HydrateType, OAuthType
    import json

    def stream_tweets(query, expansions, tweet_fields, user_fields):
        
        try:
            o = TwitterOAuth.read_file()
            api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type=OAuthType.OAUTH2, api_version='2')

            r = api.request('tweets/search/stream/rules', {'add': [{'value':QUERY}]})
            json.dumps(r.json(), indent=2)
            if r.status_code != 201: exit()

            r = api.request('tweets/search/stream/rules', method_override='GET')
            json.dumps(r.json(), indent=2)
            if r.status_code != 200: exit()

            r = api.request('tweets/search/stream', {
                    'expansions': expansions,
                    'tweet.fields': tweet_fields,
                    'user.fields': user_fields,
                },
                hydrate_type=HydrateType.APPEND)

            print(f'[{r.status_code}] START...')
            inicio = time.strftime('%H:%M:%S', time.localtime())
            print("La busqueda empezo a la/s --> " + inicio)

            
            contador_de_tweets = 0
            contador_de_tamanio = 0
            info = {}
            for item in r:
                for c,v in item.items():
                    try:
                        info[v['conversation_id']] = {'texto' : v['text'], 'nombre_oficial' : v['author_id_hydrate']['name'], 'cuenta' : v['author_id_hydrate']['username'], 'id_usuario' : v['author_id'], 'fecha' : v['created_at']}
                        if 'location' in v['author_id_hydrate']:
                            info[v['conversation_id']]['ubicacion'] = v['author_id_hydrate']['location']
                        if 'source' in v:
                            info[v['conversation_id']]['fuente'] = v['source']
                        contador_de_tweets += 1
                        print("Tweets encontrados hasta el momento --> " + str(contador_de_tweets))
                        contador_de_tamanio += sys.getsizeof(info[v['conversation_id']])
                        print("Tamano del tweet hasta el momento -->  " + str(contador_de_tamanio) + ' bytes\n')

                        if contador_de_tweets == 1000:
                            contador_de_tweets = 0
                            with open('corpus.json',"r", encoding="utf-8") as file_corpus:
                                datos_previos = json.load(file_corpus)
                                datos_previos.update(info)
                                print('-------------------------------------------')
                                print("BACKUP: Cantidad total de tweets almacenados: "+str(len(datos_previos)))
                                print('-------------------------------------------'+ '\n')

                            with open('corpus.json',"w", encoding="utf-8") as file_corpus:
                                jsonobj = json.dumps(datos_previos, indent=2)
                                file_corpus.write(jsonobj)
                        
                    except Exception as e:
                        print(e)
                    
        except KeyboardInterrupt:
            print('\nDone!')
            print("La busqueda empezo a la/s --> " + inicio)
            print("La busqueda termino a la/s --> " + time.strftime('%H:%M:%S', time.localtime()))
            print("Tweets encontrados --> " + str(contador_de_tweets))
            print("Tamanio total de los tweets --> " + str(contador_de_tamanio)+ ' bytes')
            try:
                with open('corpus.json',"r", encoding="utf-8") as file_corpus:
                    datos_previos = json.load(file_corpus)
                    datos_previos.update(info)
                    print("Cantidad total de tweets almacenados: "+str(len(datos_previos)))

                with open('corpus.json',"w", encoding="utf-8") as file_corpus:
                    jsonobj = json.dumps(datos_previos, indent=2)
                    file_corpus.write(jsonobj)
            except FileNotFoundError as e:
                with open('corpus.json',"w", encoding="utf-8") as file_corpus:
                    jsonobj = json.dumps(info, indent=2)
                    file_corpus.write(jsonobj)

        except TwitterRequestError as e:
            print(f'\n{e.status_code}')
            for msg in iter(e):
                print(msg)

        except TwitterConnectionError as e:
            print(e)

        except Exception as e:
            print(e)

    QUERY = '(vacuna OR covid OR pandemia OR #covid-19 OR #covid19 OR Sputnik OR Astrazeneca OR Sinopharm) (-muerte) lang:es (-is:retweet) (-is:reply)'
    EXPANSIONS = 'author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id,attachments.media_keys,attachments.poll_ids,geo.place_id,entities.mentions.username'
    TWEET_FIELDS='author_id,conversation_id,created_at,entities,geo,id,lang,public_metrics,source,text'
    USER_FIELDS='created_at,description,entities,location,name,profile_image_url,public_metrics,url,username'
    stream_tweets(QUERY, EXPANSIONS, TWEET_FIELDS, USER_FIELDS)