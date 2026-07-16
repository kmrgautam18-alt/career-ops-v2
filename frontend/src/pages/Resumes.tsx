import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  FileText, Upload, Trash2, Loader2, Download, File,
  CheckCircle2,
} from 'lucide-react';
import { resumesApi } from '../api/client';

interface Resume {
  id: number;
  title?: string;
  original_filename?: string;
  file_name?: string;
  mime_type?: string;
  file_type?: string;
  file_size?: number;
  upload_status?: string;
  status?: string;
  created_at?: string;
}

export function Resumes() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchResumes = () => {
    setLoading(true);
    resumesApi.list()
      .then((res) => setResumes(Array.isArray(res.data.data) ? res.data.data : []))
      .catch(() => setResumes([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchResumes(); }, []);

  const handleUpload = async (file: File) => {
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', file.name.replace(/\.[^/.]+$/, ''));
    try {
      await resumesApi.upload(formData);
      fetchResumes();
    } catch (err) {
      console.error('Upload failed', err);
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleUpload(file);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleUpload(file);
  };

  const handleDelete = async (id: number) => {
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
    <div className="space-y-7 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-2xl sm:text-3xl font-bold text-text-heading">Resumes</h1>
        <p className="text-text-muted mt-1">Upload and manage your resume arsenal</p>
      </motion.div>

      {/* Upload Area */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.doc"
          onChange={handleFileChange}
          className="hidden"
        />
        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`
            relative p-10 sm:p-14 rounded-2xl border-2 border-dashed cursor-pointer
            transition-all duration-300 overflow-hidden group
            ${dragOver
              ? 'border-primary/60 bg-primary-light'
              : 'border-border/40 bg-surface hover:border-primary/30 hover:bg-surface-light'
            }
            ${uploading ? 'pointer-events-none opacity-70' : ''}
          `}
        >
          {/* Hover glow */}
          <div className="absolute -top-32 -right-32 w-64 h-64 rounded-full bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-3xl pointer-events-none" />

          <div className="relative flex flex-col items-center gap-4">
            {uploading ? (
              <>
                <div className="w-16 h-16 rounded-2xl bg-primary-light flex items-center justify-center">
                  <Loader2 className="w-8 h-8 text-primary animate-spin" />
                </div>
                <div className="text-center">
                  <p className="text-text-heading font-medium">Uploading...</p>
                  <p className="text-text-muted text-sm mt-1">Processing your resume</p>
                </div>
                <div className="w-48 h-1.5 rounded-full bg-border overflow-hidden">
                  <div className="h-full w-1/3 rounded-full bg-gradient-to-r from-primary to-accent animate-shimmer" />
                </div>
              </>
            ) : (
              <>
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-accent/30 flex items-center justify-center group-hover:scale-110 transition-transform duration-300 shadow-lg shadow-primary-glow/20">
                  <Upload className={`w-8 h-8 text-primary transition-all duration-300 ${dragOver ? 'translate-y-1' : ''}`} />
                </div>
                <div className="text-center">
                  <p className="text-text-heading font-medium">
                    {dragOver ? 'Drop your resume here' : 'Upload Resume'}
                  </p>
                  <p className="text-text-muted text-sm mt-1">
                    Drop a file or click to browse &mdash; PDF, DOCX (Max 10 MB)
                  </p>
                </div>
                <div className="flex items-center gap-2 text-xs text-text-muted/60">
                  <CheckCircle2 className="w-3 h-3 text-success" />
                  <span>AI-powered parsing & analysis</span>
                </div>
              </>
            )}
          </div>
        </div>
      </motion.div>

      {/* Resume List */}
      {loading ? (
        <div className="flex justify-center py-16">
          <div className="flex flex-col items-center gap-3">
            <Loader2 className="w-8 h-8 text-primary animate-spin" />
            <p className="text-text-muted text-sm">Loading resumes...</p>
          </div>
        </div>
      ) : resumes.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-16 glass-panel rounded-2xl"
        >
          <div className="w-16 h-16 rounded-2xl bg-primary-light flex items-center justify-center mb-4">
            <FileText className="w-8 h-8 text-primary" />
          </div>
          <p className="text-text-heading font-medium">No resumes yet</p>
          <p className="text-text-muted text-sm mt-1">Upload your first resume to get started</p>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="grid gap-3.5"
        >
          {resumes.map((resume, i) => (
            <motion.div
              key={resume.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
              className="group relative p-5 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 overflow-hidden"
            >
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
              </div>

              <div className="relative flex items-center justify-between gap-4">
                <div className="flex items-center gap-4 min-w-0 flex-1">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center flex-shrink-0 shadow-lg">
                    <File className="w-6 h-6 text-white" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-text-heading truncate">
                      {resume.title || resume.original_filename || resume.file_name}
                    </p>
                    <div className="flex items-center gap-3 mt-1.5 text-xs text-text-muted">
                      {resume.mime_type && (
                        <span className="px-2 py-0.5 rounded-full bg-surface-lighter text-text-muted">
                          {resume.mime_type}
                        </span>
                      )}
                      {resume.file_size && (
                        <span>{formatSize(resume.file_size)}</span>
                      )}
                      {resume.upload_status && (
                        <span className="flex items-center gap-1 text-success">
                          <CheckCircle2 className="w-3 h-3" />
                          {resume.upload_status}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-1.5 flex-shrink-0">
                  <button
                    onClick={() => window.open(`/api/v1/resumes/${resume.id}/download`, '_blank')}
                    className="p-2.5 rounded-xl text-text-muted hover:text-text-heading hover:bg-surface-lighter transition-all"
                  >
                    <Download className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(resume.id)}
                    className="p-2.5 rounded-xl text-text-muted hover:text-danger hover:bg-danger-light transition-all"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}
