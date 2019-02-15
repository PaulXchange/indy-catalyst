import os
import json
import logging
import requests

# LEDGER_URL = os.environ.get('LEDGER_URL')
# if not LEDGER_URL:
#     raise Exception('LEDGER_URL must be set.')


class ClaimParser(object):
    """
    Parses a generic claim.
    """

    def __init__(self, claim: str) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__orgData = claim
        self.__parse()

    def __parse(self):
        self.__logger.debug(
            "\n============================================================================\n" +
            "Parsing claim:\n" +
            "----------------------------------------------------------------------------\n" +
            "{0}\n".format(json.dumps(json.loads(self.__orgData), indent=2)) +
            "============================================================================\n")

        data = json.loads(self.__orgData)
        self.__claim_type = data["claim_type"]
        self.__claim = data["claim_data"]
        self.__issuer_did = data["issuer_did"]
        self.__cred_def = data["cred_def"]
        self.__cred_req_metadata = data["cred_req_metadata"]

        # # Get schema from ledger
        # # Once we upgrade to later version of
        # try:
        #   resp = requests.get('{}/ledger/domain/{}'.format(
        #       LEDGER_URL,
        #       self.__claim['schema_seq_no']
        #   ))
        #   self.__schema = resp.json()
        # except:
        #   self.__schema = None

    def getField(self, field):
        value = None
        try:
            value = self.__claim["values"][field]['raw']
        except:
            pass

        return value

    @property
    def schemaName(self) -> str:
        return self.__claim_type

    # @property
    # def schema(self) -> str:
    #     return self.__schema

    @property
    def issuerDid(self) -> str:
        return self.__issuer_did

    @property
    def credDef(self) -> str:
        return self.__cred_def

    @property
    def credDefMeta(self) -> str:
        return self.__cred_req_metadata

    @property
    def json(self) -> str:
        return json.dumps(self.__claim)
