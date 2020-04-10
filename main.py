import ftplib
import os

from builders.elasticsearch_document_builder import create_document
from config.govtech_ftp_config import GovTechFTPConfig
from es_utils.connector import ElasticConnector
from ftp.FtpReader import FtpReader
from ftp.ftp_walk import FTPWalk
from processing.patent_parser import PatentParser

if __name__ == "__main__":

    ftp_reader = FtpReader()

    govtech_config = GovTechFTPConfig()

    es_connection = ElasticConnector()
    es_connection.connect()

    ftp_connection = ftplib.FTP(host=govtech_config.host)
    ftp_connection.login(user=govtech_config.username,
                         passwd=govtech_config.password)
    ftp_walk = FTPWalk(ftp_connection)
    for path_info in ftp_walk.walk():
        print(path_info[0])

        for file in path_info[2]:
            print(file)
            if file.endswith(".pdf"):
                path_to_current_file = os.path.join(path_info[0], file)
                try:
                    ftp_connection.retrbinary(f'RETR {path_to_current_file}', ftp_reader.read)
                except Exception as e:
                    print("FTP:", e, path_to_current_file)
                    with open("log.txt", "a") as log:
                        log.write(f"FTP: {path_to_current_file} \n")
                    continue
                parser = PatentParser(name=file, folder=path_to_current_file, data=ftp_reader.data)

                try:
                    document_text = parser.parse()
                except Exception as e:
                    print("Tika:", e, path_to_current_file)
                    with open("log.txt", "a") as log:
                        log.write(f"Tika: {path_to_current_file} \n")
                    continue

                try:
                    es_document = create_document(filename=file, path=path_info[0], text=document_text)
                    es_connection.add_document(es_document)
                except Exception as e:
                    print("ES:", e, path_to_current_file)
                    with open("log.txt", "a") as log:
                        log.write(f"FTP: {path_to_current_file} \n")
                print("file parsed and saved")
