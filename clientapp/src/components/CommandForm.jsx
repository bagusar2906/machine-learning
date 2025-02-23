import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css"; // Import Bootstrap Icons

export default function CommandForm() {
  const [formData, setFormData] = useState({
    command: "",
    method: "Concentrate",
    currentVolume: "0.00",
    mwco: "5",
    initialConcentrate: "0.1",
    finalVolume: "0.00",
   /*  startExchange: "0.00",
    stepSize: "1",
    exchangeVolume: "0.00",
    currentBufferVolume: "0.00", */
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showToast, setShowToast] = useState(false);
 

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

    formData.mwco = parseInt(formData.mwco);
    formData.currentVolume = parseFloat(formData.currentVolume);
    formData.finalVolume = parseFloat(formData.finalVolume);
    formData.initialConcentrate = parseFloat(formData.initialConcentrate);
    formData.finalConcentrate = parseFloat(formData.finalConcentrate);
    formData.startExchange = parseFloat(formData.startExchange);
    formData.stepSize = parseFloat(formData.stepSize);
    formData.exchangeVolume = parseFloat(formData.exchangeVolume);
    formData.currentBufferVolume = parseFloat(formData.currentBufferVolume);

   
    
    setIsLoading(true);

    try {
      console.log("Submitting data:", JSON.stringify(formData));
      const response = await fetch("/api/train", {
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
          currentVolume: 0.0,
          currentBufferVolume: 0.0,
          initialConcentrate: 0.1,
          finalVolume: 0,
          finalConcentrate: 0,
          startExchange: 0,
          stepSize: 1,
          exchangeVolume: 0,
          mwco: 0
        });
      } else {
        setError("An unexpected error occurred. Please try again.");
        setShowToast(true);
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
    <div className="container d-flex justify-content-center align-items-center" style={{ height: "auto", paddingTop: "10px", paddingBottom: "10px" }}>
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
      {/* Error Toast using Bootstrap */}
      {showToast && (
        <div className="position-fixed top-0 start-50 translate-middle-x p-3" style={{ zIndex: 1050 }}>
          <div className="toast show align-items-center text-white bg-danger border-0" role="alert">
            <div className="d-flex">
              <div className="toast-body">
                {error}
              </div>
              <button type="button" className="btn-close btn-close-white me-2 m-auto" onClick={() => setShowToast(false)}></button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
