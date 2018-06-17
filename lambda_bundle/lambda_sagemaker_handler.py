import boto3
from scipy.sparse import coo_matrix
import json

def lambda_handler(event, context):
    # TODO implement
    endpoint = os.environ['sagemaker_endpoint']
    moviesList = [11164, 1194, 1223, 1224, 1246, 1311, 1347, 1413, 1538, 1771]
    cooMatrix = convert_to_matrix(moviesList)
    return invoke_sagemaker(endpoint, cooMatrix)


def convert_to_matrix(moviesList):
    # TODO Too bad this is hardcoded!!. Needs to be aligned with the no:of features in the movies dataset, which is no_users + no_nmovies
    nbUsers = 943
    nbMovies = 1682
    # TODO Validate that the movie list must be within the movies Range.
    nbFeatures = nbUsers+nbMovies
    nbRatings = len(moviesList)
    X = coo_matrix((nbRatings, nbFeatures), dtype='float32')

    line = 0
    userId = 100

    for movieId in moviesList:
        X[line, int(userId)-1] = 1
        X[line, int(nbUsers)+int(movieId)-1] = 1
        line = line+1

    return X

def invoke_sagemaker(endpoint, cooMatrix):
    client = boto3.client('runtime.sagemaker')
    json_data = fm_serializer(cooMatrix.toarray())
    response = client.invoke_endpoint(
        EndpointName=endpoint,
        Body=json_data ,
        ContentType='application/json'
    )
    return response.Body


def fm_serializer(data):
    js = {'instances': []}
    for row in data:
        js['instances'].append({'features': row.tolist()})
    return json.dumps(js)
