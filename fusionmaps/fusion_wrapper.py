import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class FusionWrapper(object):

    def __init__(self, credentials, tableId):
        self._credentials_file = credentials
        self.service = self._get_service()
        self.tableId = tableId

    def _get_service(self):
        scopes = ['https://www.googleapis.com/auth/fusiontables']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self._credentials_file, scopes=scopes)
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build("fusiontables", "v2", http=http)
        return service

    def address_exist(self, lat, lng):
        q = self.service.query()
        template_sql = "SELECT * FROM {tableId} WHERE Location='{location}'"
        sql = template_sql.format(
            tableId=self.tableId,
            location=','.join([lat, lng])
        )
        res = q.sqlGet(sql=sql).execute()
        return 'rows' in res

    def add_address(self, address, lat, lng):
        q = self.service.query()
        template_sql = """
            INSERT INTO
                {tableId}
                (Text, Location)
            VALUES
                ('{address}', '{location}')"""
        sql = template_sql.format(
            tableId=self.tableId,
            address=address,
            location=','.join([lat, lng])
        )
        print(sql)
        q.sql(sql=sql).execute()

    def remove_all_addresses(self):
        q = self.service.query()
        template_sql = """ DELETE FROM {tableId} """
        sql = template_sql.format(tableId=self.tableId)
        q.sql(sql=sql).execute()
