import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { FileText, Upload, Trash2, Loader2, Download, File } from 'lucide-react';
import { resumesApi } from '../api/client';

interface Resume {
  id: number;
  file_name: string;
  file_type?: string;
  file_size?: number;
  status?: string;
  created_at?: string;
}

export function Resumes() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchResumes = () => {
    setLoading(true);
    resumesApi.list()
      .then((res) => setResumes(Array.isArray(res.data.data) ? res.data.data : []))
      .catch(() => setResumes([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchResumes(); }, []);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      await resumesApi.upload(formData);
      fetchResumes();
    } catch (err) {
      console.error('Upload failed', err);
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this resume?')) return;
    try {
      await resumesApi.delete(id);
      fetchResumes();
    } catch (err) {
      console.error('Failed to delete resume', err);
    }
  };

  const formatSize = (bytes?: number) => {
    if (!bytes) return '';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-text-heading">Resumes</h1>
        <p className="text-text mt-1">Upload and manage your resumes</p>
      </div>

      {/* Upload Area */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.doc"
          onChange={handleUpload}
          className="hidden"
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className="w-full p-8 rounded-xl border-2 border-dashed border-border hover:border-primary/50 bg-surface hover:bg-surface-light transition-all duration-200 group cursor-pointer disabled:opacity-50"
        >
          {uploading ? (
            <div className="flex flex-col items-center gap-3">
              <Loader2 className="w-8 h-8 text-primary animate-spin" />
              <p className="text-sm text-text">Uploading...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-primary-light flex items-center justify-center group-hover:scale-110 transition-transform">
                <Upload className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium text-text-heading">Upload Resume</p>
                <p className="text-xs text-text mt-1">PDF, DOCX — Max 10 MB</p>
              </div>
            </div>
          )}
        </button>
      </motion.div>

      {/* Resume List */}
      {loading ? (
        <div className="flex justify-center py-12"><Loader2 className="w-8 h-8 text-primary animate-spin" /></div>
      ) : resumes.length === 0 ? (
        <div className="text-center py-12">
          <FileText className="w-12 h-12 text-text/40 mx-auto mb-3" />
          <p className="text-text">No resumes uploaded yet.</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {resumes.map((resume, i) => (
            <motion.div
              key={resume.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex items-center justify-between p-4 rounded-xl bg-surface border border-border hover:border-primary/20 transition-all duration-200"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-accent-light flex items-center justify-center">
                  <File className="w-5 h-5 text-accent" />
                </div>
                <div>
                  <p className="text-sm font-medium text-text-heading">{resume.file_name}</p>
                  <div className="flex items-center gap-2 text-xs text-text">
                    {resume.file_type && <span>{resume.file_type}</span>}
                    {resume.file_size && <span>{formatSize(resume.file_size)}</span>}
                    {resume.status && (
                      <span className="px-1.5 py-0.5 rounded bg-primary-light text-primary text-xs">
                        {resume.status}
                      </span>
                    )}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => window.open(`/api/v1/resumes/${resume.id}/download`, '_blank')}
                  className="p-2 rounded-lg text-text hover:text-text-heading hover:bg-surface-light transition-colors"
                >
                  <Download className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDelete(resume.id)}
                  className="p-2 rounded-lg text-text hover:text-danger hover:bg-danger/10 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
