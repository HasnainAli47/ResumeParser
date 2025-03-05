import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { CircularProgress, Button } from "@mui/material";
import { toast } from "react-toastify";
import { api } from "../api/api";

const ResumeUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const { getRootProps, getInputProps } = useDropzone({
    accept: ".pdf,.doc,.docx",
    multiple: false,
    onDrop: (acceptedFiles) => {
      setSelectedFile(acceptedFiles[0]);
      setUploadProgress(0);
      toast.info("File ready for upload.");
    },
  });

  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setIsUploading(true);
      toast.info("Uploading file...");

      const response = await api.post('/upload/', formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percent);
        },
      });

      if (response.status >= 200 && response.status < 300) {
        toast.success("Upload successful!");
        setSelectedFile(null);
        setUploadProgress(0);
      } else {
        toast.error("Upload failed. Please try again.");
      }
    } catch (error) {
      toast.error("Error uploading file.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-xl shadow-lg w-96 text-center">
        <h2 className="text-lg font-semibold mb-4 text-gray-700">Upload Your Resume</h2>
        
        <div {...getRootProps()} className="border-2 border-dashed border-gray-400 p-6 rounded-lg bg-gray-50 cursor-pointer hover:bg-gray-100 transition">
          <input {...getInputProps()} />
          <p className="text-gray-500">Drag & drop your resume here, or click to browse</p>
        </div>

        {selectedFile && (
          <p className="mt-3 text-sm text-gray-600">Selected: {selectedFile.name}</p>
        )}

        {uploadProgress > 0 && <CircularProgress variant="determinate" value={uploadProgress} className="mt-4" />}

        <Button 
          variant="contained" 
          color="primary" 
          className="mt-4 w-full" 
          onClick={handleUpload} 
          disabled={!selectedFile || isUploading}
        >
          {isUploading ? "Uploading..." : "Upload"}
        </Button>
      </div>
    </div>
  );
};

export default ResumeUpload;
