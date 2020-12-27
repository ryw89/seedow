use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

/// Check if a string has a substring.
fn has_substr(string: String, substr: &str) -> bool {
    if string.contains(substr) {
        return true;
    }
    return false;
}

/// Check if a vector of strings contains a substring.
#[pyfunction]
fn has_substr_vec(strings: Vec<String>, substr: &str) -> PyResult<Vec<bool>> {
    let mut out = Vec::new();
    for s in strings {
        out.push(has_substr(s, substr));
    }
    Ok(out)
}

#[pymodule]
fn seedow_rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(has_substr_vec))?;

    Ok(())
}
