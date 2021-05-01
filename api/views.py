from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Artist, Album, Track
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from base64 import b64encode
# Create your views here.
host = "https://tarea2app.herokuapp.com"


@api_view(['GET', 'POST'])
def artists_list(request):
    if request.method == 'GET':
        artists = Artist.objects.all()
        context_serializer = {'request': request}
        serializer = ArtistSerializer(artists, many=True, context=context_serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        try:
            a = request.data['name']
            b = request.data['age']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if type(a) != str or type(b) != int:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        codificado = b64encode(request.data['name'].encode()).decode('utf-8')
        if len(codificado) > 22:
            codificado = codificado[:22]
        a = request.build_absolute_uri()

        request.data['self'] = f"{host}/artists/{codificado}"
        request.data['albums'] = f"{host}/artists/{codificado}/albums"
        request.data['tracks'] = f"{host}/artists/{codificado}/tracks"
        request.data['id'] = codificado
        request.data['idd'] = codificado
        try:
            artista = Artist.objects.get(idd=codificado)
        except Artist.DoesNotExist:
            serializer_context = {'request': request}
            serializer = ArtistSerializer(data=request.data, context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            serializer = ArtistSerializer(artista, many=False)
            return Response(serializer.data, status=status.HTTP_409_CONFLICT)


@api_view(['GET', 'DELETE'])
def artists_detail(request, pk):
    if request.method == 'GET':
        try:
            artist = Artist.objects.get(idd=pk)
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        context_serializer = {'request': request}
        serializer = ArtistSerializer(artist, many=False, context=context_serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        print("______________________________________________________ENTR0")
        try:
            artist = Artist.objects.get(idd=pk)
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# ALBUM VIEWS
@api_view(['GET'])
def albums_list(request):
    albums = Album.objects.all()
    context_serializer = {'request': request}
    serializer = AlbumSerializer(albums, many=True, context=context_serializer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def albums_list_by_artist(request, pk):
    if request.method == 'GET':
        try:
            artist = Artist.objects.get(idd=pk)
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            albums = Album.objects.filter(artist_id=pk)
        except Album.DoesNotExist:
            return Response(status=status.HTTP_200_OK)
        context_serializer = {'request': request}
        serializer = AlbumSerializer(albums, context=context_serializer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method=='POST':
        try:
            a = request.data['name']
            b = request.data['genre']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if type(a) != str or type(b) != str:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        codificado = f"{request.data['name']}:{pk}"
        codificado = b64encode(codificado.encode()).decode('utf-8')
        if len(codificado) > 22:
            codificado = codificado[:22]


        try:
            album = Album.objects.get(idd=codificado)

        except Album.DoesNotExist:
            request.data['gen'] = request.data['genre']
            request.data['id'] = codificado
            request.data['idd'] = codificado
            request.data['artist_id'] = pk
            request.data['genre'] = request.data['gen']
            try:
                artist = Artist.objects.get(idd=pk)
            except Artist.DoesNotExist:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            request.data['artist'] = f"{host}/artists/{pk}"
            request.data['self'] = f"{host}/albums/{codificado}"
            request.data['tracks'] = f"{host}/albums/{codificado}/tracks"
            serializer_context = {'request': request}
            serializer = AlbumSerializer(data=request.data, context=serializer_context)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            serializer = AlbumSerializer(album, many=False)
            return Response(serializer.data, status=status.HTTP_409_CONFLICT)




@api_view(['GET', 'DELETE'])
def albums_detail(request, pk):
    if request.method == 'GET':
        try:
            albums = Album.objects.get(idd=pk)
        except Album.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        context_serializer = {'request': request}
        serializer = AlbumSerializer(albums, many=False, context=context_serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        try:
            album = Album.objects.get(idd=pk)
        except Album.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            album.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def play_artist_tracks(request, pk):
    try:
        artist = Artist.objects.get(idd=pk)
    except Artist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        tracks = Track.objects.filter(artist_id=pk)
    except Track.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    print("artista si existe")
    for t in tracks:
        print("chupalo dj")
        t.times_played += 1
        t.save()
    return Response(status=status.HTTP_200_OK)


# TRACKS VIEWS
@api_view(['GET'])
def tracks_list(request):
    tracks = Track.objects.all()
    context_serializer = {'request': request}
    serializer = TrackSerializer(tracks, many=True, context=context_serializer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def tracks_detail(request, pk):
    if request.method == 'GET':
        try:
            tracks = Track.objects.get(idd=pk)
        except Track.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        context_serializer = {'request': request}
        serializer = TrackSerializer(tracks, many=False, context=context_serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        try:
            track = Track.objects.get(idd=pk)
        except Track.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def play_album_tracks(request, pk):
    try:
        album = Album.objects.get(idd=pk)
    except Album.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        tracks = Track.objects.filter(album_id=pk)
    except Track.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    for t in tracks:
        t.times_played += 1
        t.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def tracks_list_by_album(request, pk):
    if request.method == 'GET':
        try:
            album = Album.objects.get(idd=pk)
        except Album.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            tracks = Track.objects.filter(album_id=pk)
        except Track.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)
        context_serializer = {'request': request}
        serializer = TrackSerializer(tracks, context=context_serializer, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            a = request.data['name']
            b = request.data['duration']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        tipo = type(b) == float or type(b) == int

        if type(a) != str or not tipo:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        codificado = f"{request.data['name']}:{pk}"
        codificado = b64encode(codificado.encode()).decode('utf-8')
        if len(codificado) > 22:
            codificado = codificado[:22]
        request.data['id'] = codificado
        request.data['idd'] = codificado
        try:
            track = Track.objects.get(idd=codificado)
        except Track.DoesNotExist:
            request.data['album_id'] = pk
            request.data['times_played'] = 0

            request.data['self'] = f"{host}/tracks/{codificado}"
            request.data['album'] = f"{host}/albums/{pk}"
            print(pk)
            try:
                album = Album.objects.get(idd=pk)
            except Album.DoesNotExist:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            artista = str(Album.objects.get(idd=pk).artist_id)
            artista_cod = b64encode(artista.encode()).decode('utf-8')
            request.data['artist_id'] = artista_cod
            if len(artista_cod) > 22:
                request.data['artist_id'] = artista_cod[0:22]
            print(artista_cod)
            request.data['artist'] = f"{host}/artists/{artista_cod}"
            serializer_context = {'request': request}
            serializer = TrackSerializer(data=request.data, context=serializer_context)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            serializer = TrackSerializer(track, many=False)
            return Response(serializer.data, status=status.HTTP_409_CONFLICT)



@api_view(['GET'])
def tracks_list_by_artist(request, pk):
    try:
        artist = Artist.objects.get(idd=pk)
    except Artist.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)
    tracks = Track.objects.filter(artist_id=pk)
    context_serializer = {'request': request}
    serializer = TrackSerializer(tracks, many=True, context=context_serializer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def play_track(request, pk):
    try:
        track = Track.objects.get(idd=pk)
    except Track.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    track.times_played += 1
    track.save()
    return Response(status=status.HTTP_200_OK)

