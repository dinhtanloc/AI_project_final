from unittest import TestCase
from unittest.mock import patch
from utils.prepare_vectodb import PrepareVectorDB

class TestPrepareVectorDB(TestCase):

    @patch('utils.prepare_vectodb.pymongo.MongoClient')
    def test_run(self, mock_mongo_client):
        mock_db = mock_mongo_client.return_value
        mock_db.__getitem__.return_value = mock_db
        
        prepare_db_instance = PrepareVectorDB(
            doc_dir='some_dir',
            chunk_size=1000,
            chunk_overlap=200,
            mongodb_uri='mongodb://localhost:27017',
            db_name='test_db',
            collection_name='test_collection'
        )

        prepare_db_instance.run()

        mock_mongo_client.assert_called_once_with('mongodb://localhost:27017')
        
        self.assertEqual(mock_db.test_collection.insert_one.call_count, 1)

