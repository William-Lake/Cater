from pandasql import sqldf
import pandas as pd

QUERY = "QUERY"
DFS = "DFS"


class QueryExecutor:
    def execute_query_against_dfs(self, query, dfs):

        # TODO Exception handling re: empty dfs

        return sqldf(query, dfs)
