import pytest
import pandas as pd


@pytest.fixture
def matriz_exemplo():
    return pd.DataFrame({
        "processo":           ["Agricultura", "Transporte", "Industria"],
        "energia_solar_sej":  [1.50e+15, 3.20e+14, 6.80e+15],
        "energia_quimica_sej":[2.30e+14, 9.10e+13, 1.40e+15],
        "biomassa_sej":       [8.70e+14, 0,        2.10e+14],
        "produto":            ["graos", "combustivel", "manufaturado"],
    })


@pytest.fixture
def csv_padrao(tmp_path):
    csv = tmp_path / "lci.csv"
    csv.write_text(
        "processo,energia_solar_sej,energia_quimica_sej,biomassa_sej,produto\n"
        "Agricultura,1.50e+15,2.30e+14,8.70e+14,graos\n"
        "Transporte,3.20e+14,9.10e+13,0,combustivel\n"
        "Industria,6.80e+15,1.40e+15,2.10e+14,manufaturado\n"
    )
    return csv


@pytest.fixture
def resultados_exemplo():
    return {
        "Agricultura": 2.73e+15,
        "Transporte":  4.32e+14,
        "Industria":   8.83e+15,
    }
