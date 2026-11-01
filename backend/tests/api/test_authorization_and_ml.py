import io
import uuid

from fastapi.testclient import TestClient

from app.core.config import settings


def test_unauthenticated_requests_rejected(client: TestClient):
    # Candidate endpoints
    assert client.get("/api/v1/candidates/me").status_code in (401, 403)
    assert client.post("/api/v1/candidates/me/resume").status_code in (401, 403)
    assert client.get("/api/v1/candidates/me/accessibility").status_code in (401, 403)

    # Employer endpoints
    assert client.get("/api/v1/employers/me").status_code in (401, 403)
    assert client.post("/api/v1/employers/me/job-documents").status_code in (401, 403)
    assert client.get("/api/v1/employers/me/accessibility").status_code in (401, 403)


def test_employer_cannot_access_candidate_endpoints(client: TestClient, create_employer):
    emp = create_employer()

    res1 = client.get("/api/v1/candidates/me", headers=emp["headers"])
    assert res1.status_code == 403

    res2 = client.get("/api/v1/candidates/me/accessibility", headers=emp["headers"])
    assert res2.status_code == 403

    res3 = client.post("/api/v1/candidates/me/resume", headers=emp["headers"])
    assert res3.status_code == 403


def test_candidate_cannot_access_employer_endpoints(client: TestClient, create_candidate):
    cand = create_candidate()

    res1 = client.get("/api/v1/employers/me", headers=cand["headers"])
    assert res1.status_code == 403

    res2 = client.get("/api/v1/employers/me/accessibility", headers=cand["headers"])
    assert res2.status_code == 403

    res3 = client.post("/api/v1/employers/me/job-documents", headers=cand["headers"])
    assert res3.status_code == 403


def test_ml_endpoints_reject_unauthorized(client: TestClient, create_candidate, create_employer):
    cand = create_candidate()
    emp = create_employer()
    fake_id = uuid.uuid4()

    # Unauthenticated
    assert client.get(f"/api/v1/internal/ml/resumes/{fake_id}").status_code == 403
    assert client.get(f"/api/v1/internal/ml/job-documents/{fake_id}").status_code == 403
    assert client.get("/api/v1/internal/ml/pending-documents").status_code == 403

    # Candidate credentials rejected from ML boundary
    assert (
        client.get(f"/api/v1/internal/ml/resumes/{fake_id}", headers=cand["headers"]).status_code
        == 403
    )

    # Employer credentials rejected from ML boundary
    assert (
        client.get(
            f"/api/v1/internal/ml/job-documents/{fake_id}", headers=emp["headers"]
        ).status_code
        == 403
    )


def test_ml_service_key_authorized_retrieval(
    client: TestClient, create_candidate, create_employer, sample_pdf_bytes
):
    cand = create_candidate()
    emp = create_employer()

    # 1. Candidate uploads resume
    res_files = {"file": ("cand_resume.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")}
    cand_upload = client.post(
        "/api/v1/candidates/me/resume", headers=cand["headers"], files=res_files
    )
    assert cand_upload.status_code == 201
    resume_id = cand_upload.json()["id"]

    # 2. Employer uploads job doc
    job_files = {"file": ("job_spec.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")}
    emp_upload = client.post(
        "/api/v1/employers/me/job-documents", headers=emp["headers"], files=job_files
    )
    assert emp_upload.status_code == 201
    job_doc_id = emp_upload.json()["id"]

    # 3. Authorized ML team headers
    ml_headers = {"X-Internal-Service-Key": settings.INTERNAL_ML_API_KEY}

    # Retrieve resume metadata & binary
    ml_resume_res = client.get(f"/api/v1/internal/ml/resumes/{resume_id}", headers=ml_headers)
    assert ml_resume_res.status_code == 200
    assert ml_resume_res.json()["document_type"] == "RESUME"
    assert ml_resume_res.json()["original_filename"] == "cand_resume.pdf"

    ml_resume_content = client.get(
        f"/api/v1/internal/ml/resumes/{resume_id}/content", headers=ml_headers
    )
    assert ml_resume_content.status_code == 200
    assert ml_resume_content.content == sample_pdf_bytes

    # Retrieve job doc metadata & binary
    ml_job_res = client.get(f"/api/v1/internal/ml/job-documents/{job_doc_id}", headers=ml_headers)
    assert ml_job_res.status_code == 200
    assert ml_job_res.json()["document_type"] == "JOB_DOCUMENT"
    assert ml_job_res.json()["original_filename"] == "job_spec.pdf"

    ml_job_content = client.get(
        f"/api/v1/internal/ml/job-documents/{job_doc_id}/content", headers=ml_headers
    )
    assert ml_job_content.status_code == 200
    assert ml_job_content.content == sample_pdf_bytes

    # List pending documents
    ml_pending_res = client.get("/api/v1/internal/ml/pending-documents", headers=ml_headers)
    assert ml_pending_res.status_code == 200
    pending_data = ml_pending_res.json()
    assert any(j["document_id"] == job_doc_id for j in pending_data["pending_job_documents"])
    assert any(r["document_id"] == resume_id for r in pending_data["active_resumes"])


def test_admin_authorized_ml_retrieval(
    client: TestClient, create_candidate, create_admin, sample_pdf_bytes
):
    cand = create_candidate()
    admin = create_admin()

    files = {"file": ("admin_test.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")}
    cand_upload = client.post("/api/v1/candidates/me/resume", headers=cand["headers"], files=files)
    resume_id = cand_upload.json()["id"]

    # Admin access using standard Bearer token
    admin_res = client.get(f"/api/v1/internal/ml/resumes/{resume_id}", headers=admin["headers"])
    assert admin_res.status_code == 200
    assert admin_res.json()["document_type"] == "RESUME"
