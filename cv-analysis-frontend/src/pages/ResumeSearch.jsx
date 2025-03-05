import { useState } from "react";
import { TextField, Button, Chip, MenuItem, CircularProgress } from "@mui/material";
import { toast } from "react-toastify";
import { motion } from "framer-motion";
import { api } from "../api/api";

const predefinedSkills = ["Python", "Django", "React", "Machine Learning", "Data Science"];

const ResumeSearch = () => {
  const [filters, setFilters] = useState({
    skills: [],
    customSkill: "",
    min_experience: "",
    education_level: "",
    certifications: [],
  });
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [noResults, setNoResults] = useState(false);

  // Handle Search Request
  const handleSearch = async () => {
    toast.info("Searching for candidates...");
    setLoading(true);
    setSearchResults([]); // Clear previous results
    setNoResults(false); // Reset no results message

    try {
      const response = await api.post("/search/", filters);
      console.log("Search Results:", response.data.results);

      if (response.data.results.length === 0) {
        setNoResults(true);
        toast.warn("No candidates found.");
      } else {
        setSearchResults(response.data.results);
        toast.success("Candidates found!");
      }
    } catch (error) {
      toast.error("Failed to fetch candidates. Please try again.");
    }

    setLoading(false);
  };

  // Add Custom Skill
  const handleAddCustomSkill = () => {
    if (filters.customSkill.trim() && !filters.skills.includes(filters.customSkill)) {
      setFilters((prev) => ({
        ...prev,
        skills: [...prev.skills, filters.customSkill.trim()],
        customSkill: "",
      }));
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-background p-4">
      <motion.div
        className="bg-white p-6 rounded-lg shadow-md w-full max-w-lg"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-lg font-bold mb-4 text-center">Search Candidates</h2>

        {/* Experience Dropdown */}
        <TextField
          fullWidth
          select
          label="Experience (Min Years)"
          variant="outlined"
          className="mb-4"
          value={filters.min_experience}
          onChange={(e) => setFilters({ ...filters, min_experience: e.target.value })}
        >
          <MenuItem value="0">0 Month</MenuItem>
          <MenuItem value="0.5">6 Months</MenuItem>
          <MenuItem value="1">1 Year</MenuItem>
          <MenuItem value="2">2 Year</MenuItem>
          <MenuItem value="3">3 Years</MenuItem>
          <MenuItem value="5">5+ Years</MenuItem>
        </TextField>

        {/* Education Level */}
        <TextField
          fullWidth
          label="Education Level"
          variant="outlined"
          className="mb-4"
          value={filters.education_level}
          onChange={(e) => setFilters({ ...filters, education_level: e.target.value })}
        />

        {/* Skill Selection */}
        <div className="mb-4">
          <p className="text-gray-600 mb-2">Skills:</p>
          {predefinedSkills.map((skill) => (
            <Chip
              key={skill}
              label={skill}
              color={filters.skills.includes(skill) ? "primary" : "default"}
              className="m-1"
              onClick={() =>
                setFilters((prev) => ({
                  ...prev,
                  skills: prev.skills.includes(skill)
                    ? prev.skills.filter((s) => s !== skill)
                    : [...prev.skills, skill],
                }))
              }
            />
          ))}
        </div>

        {/* Custom Skill Input */}
        <div className="mb-4 flex items-center">
          <TextField
            fullWidth
            label="Enter Custom Skill"
            variant="outlined"
            value={filters.customSkill}
            onChange={(e) => setFilters({ ...filters, customSkill: e.target.value })}
            onKeyPress={(e) => e.key === "Enter" && handleAddCustomSkill()}
          />
          <Button variant="contained" color="secondary" className="ml-2" onClick={handleAddCustomSkill}>
            Add
          </Button>
        </div>

        {/* Search Button */}
        <Button variant="contained" color="primary" fullWidth onClick={handleSearch} disabled={loading}>
          {loading ? <CircularProgress size={24} color="inherit" /> : "Search"}
        </Button>
      </motion.div>

      {/* Search Results */}
      <div className="mt-6 w-full max-w-lg">
        {noResults && <p className="text-center text-gray-500">No candidates found.</p>}
        {searchResults.map((result, index) => (
          <motion.div
            key={index}
            className="bg-white p-4 rounded-lg shadow-md mb-4"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.2 }}
          >
            <h3 className="text-lg font-bold">Name: {result.name || "Not Available"}</h3>
            <p className="text-gray-600">Experience: {result?.experience?.join(", ") || "N/A"}</p>
            <p className="text-gray-500">Skills: {result?.skills?.join(", ") || "N/A"}</p>
            <p className="text-gray-500">Education: {result?.education?.join(", ") || "N/A"}</p>
            <p className="text-gray-500">Certifications: {result?.certifications?.join(", ") || "None"}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ResumeSearch;