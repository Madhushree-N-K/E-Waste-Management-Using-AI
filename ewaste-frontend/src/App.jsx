import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

// 🔹 Corner images
import c1 from "./assets/corner1.jpg";
import c2 from "./assets/corner2.webp";
import c3 from "./assets/corner3.webp";
import c4 from "./assets/corner4.webp";

// 🔹 Center image
import centerImg from "./assets/center.jpg";

function App() {
  const [showMain, setShowMain] = useState(false);

  // 🔹 NEW STATES
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowMain(true);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  // 🔹 FILE CHANGE
  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
  };

  // 🔹 PREDICT API CALL
  const handlePredict = async () => {
    if (!file) {
      alert("Please upload an image");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Prediction failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      {/* 🌍 AWARENESS SCREEN */}
      <AnimatePresence>
        {!showMain && (
          <>
            <CornerImage src={c1} top="40px" left="40px" rotate={-12} />
            <CornerImage src={c2} top="40px" right="40px" rotate={10} />
            <CornerImage src={c3} bottom="40px" left="40px" rotate={8} />
            <CornerImage src={c4} bottom="40px" right="40px" rotate={-10} />

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1, y: [0, -8, 0] }}
              transition={{ duration: 1, repeat: Infinity }}
              style={styles.centerBox}
            >
              <img src={centerImg} alt="E-waste" style={styles.centerImage} />
              <p style={styles.message}>
                Improper Disposal Of E-Waste Releases Toxic Chemicals That
                Silently Destroy Soil, Water & Human Health
              </p>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* ♻️ MAIN APP CARD */}
      <AnimatePresence>
        {showMain && (
          <motion.div
            initial={{ opacity: 0, scale: 0.85 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            style={styles.card}
          >
            <h2 style={styles.title}>E-Waste Management Using AI</h2>
            <p style={styles.subtitle}>
              Upload electronic waste image to predict type & value
            </p>

            {/* 🔹 IMAGE PREVIEW */}
            {preview && (
              <img
                src={preview}
                alt="preview"
                style={styles.preview}
              />
            )}

            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              style={styles.input}
            />

            <button
              onClick={handlePredict}
              style={styles.button}
              disabled={loading}
            >
              {loading ? "Predicting..." : "Predict"}
            </button>

            {/* 🔹 RESULT */}
            {result && (
              <div style={styles.result}>
                <p><b>Device:</b> {result.item_type}</p>
                <p><b>Confidence:</b> {(result.confidence * 100).toFixed(2)}%</p>
                <p><b>Estimated Price:</b> ₹{result.estimated_price}</p>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/* 🔹 Corner Image Component */
function CornerImage({ src, top, left, right, bottom, rotate }) {
  return (
    <motion.img
      src={src}
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0, rotate }}
      transition={{ duration: 0.8 }}
      style={{
        position: "absolute",
        width: "230px",
        top,
        left,
        right,
        bottom,
        borderRadius: "14px",
      }}
    />
  );
}

/* 🎨 STYLES */
const styles = {
  page: {
    minHeight: "100vh",
    background:
      "linear-gradient(135deg, #e8f5e9, #c8e6c9, #b2dfdb)",
    position: "relative",
    overflow: "hidden",
    fontFamily: "'Poppins', 'Segoe UI', sans-serif",
  },

  centerBox: {
    position: "absolute",
    top: "20%",
    left: "20%",
    transform: "translate(-50%, -50%)",
    textAlign: "center",
  },

  centerImage: {
    width: "520px",
    borderRadius: "22px",
  },

  message: {
    marginTop: "26px",
    fontSize: "30px",
    fontWeight: "900",
    textTransform: "uppercase",
    background:
      "linear-gradient(90deg, #1b5e20, #2e7d32)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },

  card: {
    width: "420px",
    background: "rgba(255,255,255,0.9)",
    borderRadius: "22px",
    padding: "30px",
    textAlign: "center",
    position: "absolute",
    top: "10%",
    left: "30%",
    transform: "translate(-50%, -50%)",
  },

  title: {
    fontSize: "26px",
    fontWeight: "800",
    color: "#1b5e20",
  },

  subtitle: {
    fontSize: "14px",
    marginBottom: "10px",
  },

  preview: {
    width: "100%",
    height: "220px",
    objectFit: "contain",
    marginBottom: "12px",
    borderRadius: "12px",
    background: "#f3f4f6",
  },

  input: {
    marginTop: "8px",
  },

  button: {
    marginTop: "16px",
    width: "100%",
    padding: "12px",
    borderRadius: "14px",
    border: "none",
    background: "linear-gradient(135deg, #22c55e, #16a34a)",
    color: "white",
    fontWeight: "700",
    cursor: "pointer",
  },

  result: {
    marginTop: "16px",
    padding: "12px",
    background: "#ecfdf5",
    borderRadius: "12px",
    color: "#065f46",
    fontWeight: "600",
  },
};

export default App;
