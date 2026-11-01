import io

from fastapi.testclient import TestClient


def test_candidate_profile_retrieval(client: TestClient, create_candidate):
    cand = create_candidate(name="Jane Doe")
    response = client.get("/api/v1/candidates/me", headers=cand["headers"])

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Doe"
    assert data["email"] == cand["user"].email
    assert data["user_id"] == str(cand["user"].id)


def test_candidate_profile_update(client: TestClient, create_candidate):
    cand = create_candidate(name="Initial Name")
    response = client.patch(
        "/api/v1/candidates/me",
        headers=cand["headers"],
        json={"full_name": "Updated Name", "phone": "+9876543210"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["phone"] == "+9876543210"

    # Verify retrieval reflects updates
    get_res = client.get("/api/v1/candidates/me", headers=cand["headers"])
    assert get_res.json()["full_name"] == "Updated Name"


def test_resume_upload_success_pdf(client: TestClient, create_candidate, sample_pdf_bytes):
    cand = create_candidate()
    files = {"file": ("my_resume.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")}
    response = client.post("/api/v1/candidates/me/resume", headers=cand["headers"], files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "my_resume.pdf"
    assert data["mime_type"] == "application/pdf"
    assert data["is_active"] is True
    assert data["file_size_bytes"] == len(sample_pdf_bytes)
    assert data["download_url"] is not None


def test_resume_upload_success_docx(client: TestClient, create_candidate, sample_docx_bytes):
    cand = create_candidate()
    files = {
        "file": (
            "resume_cv.docx",
            io.BytesIO(sample_docx_bytes),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    response = client.post("/api/v1/candidates/me/resume", headers=cand["headers"], files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "resume_cv.docx"
    assert data["is_active"] is True


def test_resume_upload_invalid_extension(client: TestClient, create_candidate):
    cand = create_candidate()
    files = {"file": ("malicious.exe", io.BytesIO(b"MZ\x90\x00"), "application/octet-stream")}
    response = client.post("/api/v1/candidates/me/resume", headers=cand["headers"], files=files)

    assert response.status_code == 400
    assert "Unsupported file extension" in response.json()["detail"]


def test_resume_upload_corrupt_content(client: TestClient, create_candidate):
    cand = create_candidate()
    # Extension is .pdf but content is not valid PDF
    files = {"file": ("fake.pdf", io.BytesIO(b"Hello this is plain text"), "application/pdf")}
    response = client.post("/api/v1/candidates/me/resume", headers=cand["headers"], files=files)

    assert response.status_code == 400
    assert "file header does not match PDF format" in response.json()["detail"]


def test_resume_replacement_and_deactivation(
    client: TestClient, create_candidate, sample_pdf_bytes, sample_docx_bytes
):
    cand = create_candidate()

    # 1. Upload first resume
    files1 = {"file": ("first_resume.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")}
    res1 = client.post("/api/v1/candidates/me/resume", headers=cand["headers"], files=files1)
    assert res1.status_code == 201
    id1 = res1.json()["id"]

    # 2. Upload replacement resume
    files2 = {
        "file": (
            "second_resume.docx",
            io.BytesIO(sample_docx_bytes),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    res2 = client.post("/api/v1/candidates/me/resume", headers=cand["headers"], files=files2)
    assert res2.status_code == 201
    id2 = res2.json()["id"]
    assert id1 != id2

    # 3. GET /me/resume returns the replacement resume
    active_res = client.get("/api/v1/candidates/me/resume", headers=cand["headers"])
    assert active_res.status_code == 200
    assert active_res.json()["id"] == id2
    assert active_res.json()["original_filename"] == "second_resume.docx"


def test_resume_direct_download(client: TestClient, create_candidate, sample_pdf_bytes):
    cand = create_candidate()
    files = {"file": ("download_test.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")}
    upload_res = client.post("/api/v1/candidates/me/resume", headers=cand["headers"], files=files)
    assert upload_res.status_code == 201

    download_res = client.get("/api/v1/candidates/me/resume/download", headers=cand["headers"])
    assert download_res.status_code == 200
    assert download_res.content == sample_pdf_bytes


def test_resume_deletion(client: TestClient, create_candidate, sample_pdf_bytes):
    cand = create_candidate()
    files = {"file": ("delete_me.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")}
    client.post("/api/v1/candidates/me/resume", headers=cand["headers"], files=files)

    # Delete resume
    del_res = client.delete("/api/v1/candidates/me/resume", headers=cand["headers"])
    assert del_res.status_code == 200

    # Getting resume now returns 404
    get_res = client.get("/api/v1/candidates/me/resume", headers=cand["headers"])
    assert get_res.status_code == 404


def test_candidate_resume_isolation(client: TestClient, create_candidate, sample_pdf_bytes):
    cand_a = create_candidate(name="Candidate A")
    cand_b = create_candidate(name="Candidate B")

    # Candidate A uploads resume
    files = {"file": ("cand_a_resume.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")}
    res_a = client.post("/api/v1/candidates/me/resume", headers=cand_a["headers"], files=files)
    assert res_a.status_code == 201

    # Candidate B has no resume
    res_b = client.get("/api/v1/candidates/me/resume", headers=cand_b["headers"])
    assert res_b.status_code == 404


def test_candidate_accessibility_preferences_crud(client: TestClient, create_candidate):
    cand = create_candidate()

    # 1. Initially empty
    list_res = client.get("/api/v1/candidates/me/accessibility", headers=cand["headers"])
    assert list_res.status_code == 200
    assert list_res.json() == []

    # 2. Add preference
    add_res = client.post(
        "/api/v1/candidates/me/accessibility",
        headers=cand["headers"],
        json={
            "category": "SCREEN_READER",
            "preference": "NVDA compatibility and semantic headings required",
            "details": "Requires properly labeled form elements during live interviews",
            "is_active": True,
        },
    )
    assert add_res.status_code == 201
    pref = add_res.json()
    pref_id = pref["id"]
    assert pref["category"] == "SCREEN_READER"
    assert pref["preference"] == "NVDA compatibility and semantic headings required"

    # 3. Update preference
    update_res = client.patch(
        f"/api/v1/candidates/me/accessibility/{pref_id}",
        headers=cand["headers"],
        json={"details": "Updated details: prefer JAWS or NVDA"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["details"] == "Updated details: prefer JAWS or NVDA"

    # 4. List reflects added item
    list_res2 = client.get("/api/v1/candidates/me/accessibility", headers=cand["headers"])
    assert len(list_res2.json()) == 1

    # 5. Delete preference
    del_res = client.delete(
        f"/api/v1/candidates/me/accessibility/{pref_id}",
        headers=cand["headers"],
    )
    assert del_res.status_code == 200

    # 6. List empty again
    list_res3 = client.get("/api/v1/candidates/me/accessibility", headers=cand["headers"])
    assert list_res3.json() == []


def test_candidate_cannot_modify_other_candidates_accessibility(
    client: TestClient, create_candidate
):
    cand_a = create_candidate()
    cand_b = create_candidate()

    # Candidate A creates a preference
    add_res = client.post(
        "/api/v1/candidates/me/accessibility",
        headers=cand_a["headers"],
        json={
            "category": "CAPTIONS",
            "preference": "Live CART captioning",
            "details": "English captioning",
        },
    )
    pref_id = add_res.json()["id"]

    # Candidate B attempts to update Candidate A's preference -> 404
    patch_res = client.patch(
        f"/api/v1/candidates/me/accessibility/{pref_id}",
        headers=cand_b["headers"],
        json={"preference": "Hacked"},
    )
    assert patch_res.status_code == 404

    # Candidate B attempts to delete Candidate A's preference -> 404
    del_res = client.delete(
        f"/api/v1/candidates/me/accessibility/{pref_id}",
        headers=cand_b["headers"],
    )
    assert del_res.status_code == 404
