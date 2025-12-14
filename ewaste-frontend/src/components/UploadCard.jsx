import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import ReactTooltip from "react-tooltip";
import Confetti from "react-confetti";
import { useWindowSize } from "react-use";

export default function UploadCard() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const { width, height } = useWindowSize();

  // Handle file selection
  const handleFileChange = (file) => {
    setSelectedFile(file);
    setResult(null);
  };

  // Drag & drop
  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) handleFileChange(file);
  };
  const handleDragOver = (e) => e.preventDefault();

  // Call backend
  const handlePredict = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("image", selectedFile);
    formData.append("brand", "");
    formData.append("age_months", "0");
    formData.append("condition", "good");

    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/predict/", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Backend error");

      const data = await response.json();
      setResult(data);

      // Add to history (recent uploads)
      setHistory((prev) => [
        { image: URL.createObjectURL(selectedFile), ...data },
        ...prev.slice(0, 4),
      ]);
    } catch (error) {
      console.error(error);
      alert("Prediction failed. Make sure FastAPI is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-200 via-pink-100 to-blue-50 p-4">
      {/* Confetti */}
      {result && <Confetti width={width} height={height} recycle={false} numberOfPieces={150} />}

      {/* Upload & Predict Card */}
      <motion.div
        className="bg-white p-8 rounded-3xl shadow-2xl w-96 text-center relative"
        whileHover={{ scale: 1.02 }}
      >
        <h1 className="text-3xl font-bold mb-6 text-purple-700">♻️ E-Waste Classifier</h1>

        {/* Drag & Drop */}
        <div
          className="border-2 border-dashed border-gray-300 p-6 rounded-xl mb-4 cursor-pointer hover:border-purple-400 transition relative"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onClick={() => document.getElementById("fileInput").click()}
        >
          {selectedFile ? (
            <motion.img
              src={URL.createObjectURL(selectedFile)}
              alt="Preview"
              className="w-full h-48 object-contain rounded-lg shadow-sm"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
            />
          ) : (
            <p className="text-gray-400">Drag & drop an image or click to upload</p>
          )}
          <input
            type="file"
            id="fileInput"
            accept="image/*"
            className="hidden"
            onChange={(e) => handleFileChange(e.target.files[0])}
          />
        </div>

        {/* Predict Button */}
        <motion.button
          onClick={handlePredict}
          className="bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition w-full mb-4 shadow-md"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          animate={{ backgroundColor: loading ? "#7c3aed" : "#6b21a8" }}
          transition={{ duration: 0.5 }}
        >
          {loading ? "Predicting..." : "Predict"}
        </motion.button>

        {/* Result Card */}
        <AnimatePresence>
          {result && (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              transition={{ duration: 0.3 }}
              className="bg-purple-50 p-4 rounded-lg border border-purple-200 shadow-sm text-left text-sm"
            >
              <p><strong>Device:</strong> {result.item_type}</p>
              <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(2)}%</p>
              <p><strong>Estimated Price:</strong> ₹{result.estimated_price}</p>
              <p><strong>Recyclers:</strong></p>
              <ul>
                {result.recyclers.map((r, i) => (
                  <li
                    key={i}
                    className="cursor-pointer hover:text-purple-600 hover:scale-105 transition transform"
                  >
                    {r}
                  </li>
                ))}
              </ul>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Recent Uploads Carousel */}
      {history.length > 0 && (
        <div className="mt-6 w-96">
          <h3 className="text-lg font-semibold mb-2 text-purple-700">Recent Uploads</h3>
          <Swiper spaceBetween={10} slidesPerView={2} autoplay={{ delay: 3000 }}>
            {history.map((item, idx) => (
              <SwiperSlide key={idx}>
                <div className="bg-white p-2 rounded-lg shadow-sm">
                  <img
                    src={item.image}
                    alt="History"
                    className="w-full h-24 object-contain rounded-md mb-1"
                  />
                  <p className="text-sm font-semibold">{item.item_type}</p>
                  <p className="text-xs text-gray-500">₹{item.estimated_price}</p>
                </div>
              </SwiperSlide>
            ))}
          </Swiper>
        </div>
      )}

      {/* Eco Tips */}
      <div className="mt-6 text-gray-600 text-sm">
        <p data-tip="Always recycle electronic waste responsibly! ♻️">
          💡 Hover for eco tips
        </p>
        <ReactTooltip place="top" type="dark" effect="float" delayShow={300} />
      </div>
    </div>
  );
}
