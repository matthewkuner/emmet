import os
from emmet.api.routes.materials.mpcomplete.query_operator import (
    MPCompleteGetQuery,
    MPCompletePostQuery,
)
from emmet.api.core.settings import MAPISettings

from pymatgen.core.structure import Structure

from monty.tempfile import ScratchDir
from monty.serialization import loadfn, dumpfn


def test_mpcomplete_post_query():
    op = MPCompletePostQuery()

    structure = Structure.from_file(
        os.path.join(MAPISettings().TEST_FILES, "Si_mp_149.cif")
    )

    assert op.query(
        structure=structure.as_dict(),
        public_name="Test Test",
        public_email="test@test.com",
    ) == {
        "criteria": {
            "structure": structure.as_dict(),
            "public_name": "Test Test",
            "public_email": "test@test.com",
        }
    }

    with ScratchDir("."):
        dumpfn(op, "temp.json")
        new_op = loadfn("temp.json")
        query = {
            "criteria": {
                "structure": structure.as_dict(),
                "public_name": "Test Test",
                "public_email": "test@test.com",
            }
        }
        assert (
            new_op.query(
                structure=structure.as_dict(),
                public_name="Test Test",
                public_email="test@test.com",
            )
            == query
        )

    docs = [
        {
            "structure": structure.as_dict(),
            "public_name": "Test Test",
            "public_email": "test@test.com",
        }
    ]
    assert op.post_process(docs, query) == docs


def test_mocomplete_get_query():
    op = MPCompleteGetQuery()

    assert op.query(
        public_name="Test Test",
        public_email="test@test.com",
    ) == {"criteria": {"public_name": "Test Test", "public_email": "test@test.com"}}

    with ScratchDir("."):
        dumpfn(op, "temp.json")
        new_op = loadfn("temp.json")
        assert new_op.query(
            public_name="Test Test",
            public_email="test@test.com",
        ) == {
            "criteria": {
                "public_name": "Test Test",
                "public_email": "test@test.com",
            }
        }
