import unittest
from fastapi.testclient import TestClient
from app.routers import genotools_router


class GenoToolsRouterTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(genotools_router.router)

    def test_run_genotools_with_pfile(self):
        params = {
            "pfile": "path/to/pfile.pgen",
            "out": "path/to/output.txt",
            "callrate": 0.95,
            "sex": True,
            "het": True,
            "maf": 0.05,
        }
        response = self.client.post("/run-genotools/", json=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Job submitted")
        self.assertEqual(response.json()["command"], "genotools --callrate 0.95 --sex --het --maf 0.05 --pgen path/to/pfile.pgen --out path/to/output.txt")

    def test_run_genotools_with_bfile(self):
        params = {
            "bfile": "path/to/bfile.bgen",
            "out": "path/to/output.txt",
            "callrate": 0.95,
            "sex": True,
            "het": True,
            "maf": 0.05,
        }
        response = self.client.post("/run-genotools/", json=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Job submitted")
        self.assertEqual(response.json()["command"], "genotools --callrate 0.95 --sex --het --maf 0.05 --bgen path/to/bfile.bgen --out path/to/output.txt")

    def test_run_genotools_with_vcf(self):
        params = {
            "vcf": "path/to/vcf.vcf",
            "out": "path/to/output.txt",
            "callrate": 0.95,
            "sex": True,
            "het": True,
            "maf": 0.05,
        }
        response = self.client.post("/run-genotools/", json=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Job submitted")
        self.assertEqual(response.json()["command"], "genotools --callrate 0.95 --sex --het --maf 0.05 --vcf path/to/vcf.vcf --out path/to/output.txt")

    def test_run_genotools_with_no_geno_file(self):
        params = {
            "out": "path/to/output.txt",
            "callrate": 0.95,
            "sex": True,
            "het": True,
            "maf": 0.05,
        }
        response = self.client.post("/run-genotools/", json=params)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"][0]["msg"], "field required")

    def test_run_genotools_with_no_output_file(self):
        params = {
            "pfile": "path/to/pfile.pgen",
            "callrate": 0.95,
            "sex": True,
            "het": True,
            "maf": 0.05,
        }
        response = self.client.post("/run-genotools/", json=params)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"][0]["msg"], "field required")

    def test_create_payload(self):
        params = {
            "pfile": "path/to/pfile.pgen",
            "out": "path/to/output.txt",
            "callrate": 0.95,
            "sex": True,
            "het": True,
            "maf": 0.05,
        }
        payload = genotools_router.create_payload(**params)
        self.assertEqual(payload, {
            "pfile": "path/to/pfile.pgen",
            "out": "path/to/output.txt",
            "callrate": 0.95,
            "sex": True,
            "het": True,
            "maf": 0.05,
        })
