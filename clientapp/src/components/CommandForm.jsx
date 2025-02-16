import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css"; // Import Bootstrap Icons

export default function CommandForm() {
  const [formData, setFormData] = useState({
    command: "",
    method: "Concentrate",
    currentVolume: "",
    mwc: "5",
    initialConcentrate: "",
    finalVolume: "",
    startExchange: "",
    stepSize: "1",
    exchangeVolume: "",
    currentBufferVolume: "",
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(""); 

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "method") {
      setFormData({
        ...formData,
        method: value,
        stepSize: value === "Buffer Exchange" ? "1" : "",
      });
    } else {
      setFormData({ ...formData, [name]: value });
    }

    setError("");
  };

  const validateForm = () => {
    const { currentVolume, finalVolume } = formData;
    if (parseInt(currentVolume) < parseInt(finalVolume)) {
      setError("Current Volume cannot be less than Final Volume.");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:5000/api/train", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        console.log("Data submitted successfully!");
        // ✅ Clear form after successful submission
        setFormData({
            command: "",
            method: "Concentrate",
            currentVolume: "",
            currentBufferVolume: "",
            initialConcentrate: "",
            finalVolume: "",
            finalConcentrate: "",
            startExchange: "",
            stepSize: "",
            exchangeVolume: "",
            mwco: ""
        });
      } else {
          console.error("Submission failed.");
      }
      const data = response.json();
      console.log("API Response:", data);
    } catch (error) {
      console.error("API Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card p-4 shadow-lg rounded-4" style={{ maxWidth: "600px", width: "100%" }}>
        <h5 className="text-center mb-3">
          <i className="bi bi-robot text-primary"></i>Train Robot Command
        </h5>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label fw-semibold">Command:</label>
            <textarea
              name="command"
              value={formData.command}
              onChange={handleChange}
              className="form-control rounded-3"
              rows="3"
              placeholder="Enter command..."
            />
          </div>

          <div className="row">
            <div className="col-md-6 mb-3">
              <label className="form-label fw-semibold">Method:</label>
              <select
                name="method"
                value={formData.method}
                onChange={handleChange}
                className="form-select rounded-3"
              >
                <option value="Concentrate">Concentrate</option>
                <option value="Buffer Exchange">Buffer Exchange</option>
              </select>
            </div>
            <div className="col-md-6 mb-3">
              <label className="form-label fw-semibold">Mwco (kda):</label>
              <input
                type="number"
                step="1"
                name="mwco"
                value={formData.mwco}
                onChange={handleChange}
                className={`form-control rounded-3 ${error ? "is-invalid" : ""}`}
                placeholder="0"
              />
            </div>
          </div>

          {/* Volume Fields */}
          <div className="row">
            <div className="col-md-6 mb-3">
              <label className="form-label fw-semibold">Sample Volume (ml):</label>
              <input
                type="number"
                step="1"
                name="currentVolume"
                value={formData.currentVolume}
                onChange={handleChange}
                className={`form-control rounded-3 ${error ? "is-invalid" : ""}`}
                placeholder="0.00"
              />
            </div>
            <div className="col-md-6 mb-3">
              <label className="form-label fw-semibold">Initial Concentrate (ml/mg):</label>
              <input
                type="number"
                step="1"
                name="initialConcentrate"
                value={formData.initialConcentrate}
                onChange={handleChange}
                className="form-control rounded-3"
                placeholder="0.1"
              />
            </div>
          </div>
          
          {/* Concentrate Fields */}
          <div className="row">
            <div className="col-md-6 mb-3">
              <label className="form-label fw-semibold">Final Volume (ml):</label>
              <input
                type="number"
                step="1"
                name="finalVolume"
                value={formData.finalVolume}
                onChange={handleChange}
                className={`form-control rounded-3 ${error ? "is-invalid" : ""}`}
                placeholder="0.00"
              />
              {error && <div className="text-danger mt-1">{error}</div>}
            </div>
            <div className="col-md-6 mb-3">
              <label className="form-label fw-semibold">Final Concentrate (mg/ml):</label>
              <input
                type="number"
                step="1"
                name="finalConcentrate"
                value={formData.finalConcentrate}
                onChange={handleChange}
                className={`form-control rounded-3 ${error ? "is-invalid" : ""}`}
                placeholder="0.00"
              />
              {error && <div className="text-danger mt-1">{error}</div>}
            </div>
          </div>

          {/* Dynamic Fields (Only for Buffer Exchange) */}
          {formData.method === "Buffer Exchange" && (
            <div className="row">
              <div className="col-md-4 mb-3">
                <label className="form-label fw-semibold">Start Exchange (ml):</label>
                <input
                  type="number"
                  step="1"
                  name="startExchange"
                  value={formData.startExchange}
                  onChange={handleChange}
                  className="form-control rounded-3"
                  placeholder="0.00"
                />
              </div>
              <div className="col-md-4 mb-3">
                <label className="form-label fw-semibold">Exchange Volume (ml):</label>
                <input
                  type="number"
                  step="1"
                  name="exchangeVolume"
                  value={formData.exchangeVolume}
                  onChange={handleChange}
                  className="form-control rounded-3"
                  placeholder="0.00"
                />
              </div>
              <div className="col-md-4 mb-3">
                <label className="form-label fw-semibold">Buffer Volume (ml):</label>
                <input
                  type="number"
                  step="1"
                  name="currentBufferVolume"
                  value={formData.currentBufferVolume}
                  onChange={handleChange}
                  className="form-control rounded-3"
                  placeholder="0.00"
                />
              </div>
              <div className="col-md-4 mb-3">
                <label className="form-label fw-semibold">Step Size (ml):</label>
                <input
                  type="number"
                  step="1"
                  name="stepSize"
                  value={formData.stepSize}
                  onChange={handleChange}
                  className="form-control rounded-3"
                  placeholder="1"
                />
              </div>
            </div>
          )}

          {/* Submit Button with Loading Indicator */}
          <button
            type="submit"
            className="btn btn-primary w-100 rounded-pill mt-3"
            disabled={isLoading} 
          >
            {isLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2"></span> Submitting...
              </>
            ) : (
              <>
                <i className="bi bi-send-fill"></i> Submit Command
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
