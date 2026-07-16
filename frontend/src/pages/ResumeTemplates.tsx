import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FileText, Search, Loader2, Download, Eye, Plus, X,
  Grid3X3, List, Sparkles, ChevronRight,
  Layout, Palette, Award, TrendingUp,
} from 'lucide-react';
import apiClient from '../api/client';

interface Template {
  id: number;
  name: string;
  category: string;
  style: string;
  content: string;
  is_public: boolean;
  download_count: number;
  created_at: string | null;
}

const CATEGORY_META: Record<string, { icon: typeof FileText; gradient: string; desc: string }> = {
  general: { icon: FileText, gradient: 'from-indigo-500 to-purple-600', desc: 'All-purpose templates' },
  technical: { icon: Layout, gradient: 'from-cyan-500 to-blue-600', desc: 'For engineers & developers' },
  creative: { icon: Palette, gradient: 'from-pink-500 to-rose-600', desc: 'Design-forward layouts' },
  executive: { icon: Award, gradient: 'from-amber-500 to-orange-600', desc: 'C-suite & management' },
  entry: { icon: TrendingUp, gradient: 'from-emerald-500 to-teal-600', desc: 'Fresh graduate optimized' },
};

export function ResumeTemplates() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [createForm, setCreateForm] = useState({ name: '', category: 'general', style: 'modern', content: '' });

  useEffect(() => {
    apiClient.get('/resume-templates/')
      .then(r => setTemplates(r.data.data?.templates || []))
      .catch(() => setTemplates([]))
      .finally(() => setLoading(false));
  }, []);

  const filtered = templates.filter(t => {
    if (activeCategory && t.category !== activeCategory) return false;
    if (search && !t.name.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const categories = [...new Set(templates.map(t => t.category))];

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.post(`/resume-templates/?name=${encodeURIComponent(createForm.name)}&category=${createForm.category}&style=${createForm.style}&content=${encodeURIComponent(createForm.content)}&is_public=true`);
      const r = await apiClient.get('/resume-templates/');
      setTemplates(r.data.data?.templates || []);
      setShowCreateModal(false);
      setCreateForm({ name: '', category: 'general', style: 'modern', content: '' });
    } catch {}
  };

  const handlePreview = async (t: Template) => {
    try {
      const r = await apiClient.get(`/resume-templates/${t.id}`);
      setSelectedTemplate(r.data.data);
    } catch {}
  };

  const getCategoryMeta = (cat: string) => CATEGORY_META[cat] || { icon: FileText, gradient: 'from-gray-500 to-slate-600', desc: '' };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 text-primary animate-spin" />
          <p className="text-text-muted text-sm">Loading templates...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between flex-wrap gap-4"
      >
        <div>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 p-2.5 shadow-lg">
              <FileText className="w-full h-full text-white" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-text-heading">Resume Templates</h1>
          </div>
          <p className="text-text-muted mt-1">Browse, preview, and use professional resume templates</p>
        </div>
        <div className="flex items-center gap-2">
          {/* View toggle */}
          <div className="flex p-1 rounded-xl bg-surface border border-border/60">
            <button onClick={() => setViewMode('grid')}
              className={`p-2 rounded-lg transition-all ${viewMode === 'grid' ? 'bg-primary/10 text-primary' : 'text-text-muted hover:text-text-heading'}`}>
              <Grid3X3 className="w-4 h-4" />
            </button>
            <button onClick={() => setViewMode('list')}
              className={`p-2 rounded-lg transition-all ${viewMode === 'list' ? 'bg-primary/10 text-primary' : 'text-text-muted hover:text-text-heading'}`}>
              <List className="w-4 h-4" />
            </button>
          </div>
          <button onClick={() => setShowCreateModal(true)}
            className="group relative inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden"
          >
            <Plus className="w-4 h-4" />
            <span>Create Template</span>
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
          </button>
        </div>
      </motion.div>

      {/* Stats */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        className="flex items-center gap-4 p-4 rounded-2xl bg-surface border border-border/60 flex-wrap"
      >
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-primary" />
          <span className="text-sm text-text-heading font-medium">{templates.length}</span>
          <span className="text-xs text-text-muted">Templates</span>
        </div>
        <div className="w-px h-5 bg-border/60" />
        <div className="flex items-center gap-2">
          <Download className="w-4 h-4 text-accent" />
          <span className="text-sm text-text-heading font-medium">
            {templates.reduce((sum, t) => sum + (t.download_count || 0), 0)}
          </span>
          <span className="text-xs text-text-muted">Total Downloads</span>
        </div>
        <div className="w-px h-5 bg-border/60" />
        <div className="flex items-center gap-2">
          <Award className="w-4 h-4 text-amber-400" />
          <span className="text-sm text-text-heading font-medium">{categories.length}</span>
          <span className="text-xs text-text-muted">Categories</span>
        </div>
        {/* Search */}
        <div className="ml-auto relative flex-1 max-w-xs">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="Search templates..."
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all text-sm"
          />
        </div>
      </motion.div>

      {/* Category Tabs */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.08 }}
        className="flex gap-2 overflow-x-auto pb-2 scrollbar-none"
      >
        <button
          onClick={() => setActiveCategory(null)}
          className={`flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-sm font-medium transition-all whitespace-nowrap border ${
            !activeCategory
              ? 'bg-gradient-to-r from-primary to-accent text-white border-transparent shadow-lg shadow-primary-glow/20'
              : 'bg-surface text-text-muted border-border/60 hover:text-text-heading hover:border-border-glow/30'
          }`}
        >
          <Sparkles className="w-4 h-4" />
          All Templates
        </button>
        {categories.map(cat => {
          const meta = getCategoryMeta(cat);
          return (
            <button key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-sm font-medium transition-all whitespace-nowrap capitalize border ${
                activeCategory === cat
                  ? 'bg-gradient-to-r from-primary to-accent text-white border-transparent shadow-lg shadow-primary-glow/20'
                  : 'bg-surface text-text-muted border-border/60 hover:text-text-heading hover:border-border-glow/30'
              }`}
            >
              <meta.icon className="w-4 h-4" />
              {cat}
            </button>
          );
        })}
      </motion.div>

      {/* Empty State */}
      {filtered.length === 0 && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-20 glass-panel rounded-2xl"
        >
          <div className="w-16 h-16 rounded-2xl bg-primary-light flex items-center justify-center mb-4">
            <FileText className="w-8 h-8 text-primary" />
          </div>
          <p className="text-text-heading font-medium mb-1">No templates found</p>
          <p className="text-text-muted text-sm mb-6">
            {search ? 'Try a different search term' : 'Be the first to create a template!'}
          </p>
          {!search && (
            <button onClick={() => setShowCreateModal(true)}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury">
              <Plus className="w-4 h-4" />
              Create First Template
            </button>
          )}
        </motion.div>
      )}

      {/* Template Grid/List */}
      {viewMode === 'grid' ? (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((template, i) => {
            const meta = getCategoryMeta(template.category);
            return (
              <motion.div
                key={template.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
                className="group relative p-5 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 overflow-hidden cursor-pointer"
                onClick={() => handlePreview(template)}
              >
                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                  <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
                </div>
                <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-3xl" />

                <div className="relative">
                  {/* Preview area */}
                  <div className="aspect-[3/4] mb-4 rounded-xl bg-gradient-to-br from-surface-light/50 to-surface-lighter/30 border border-border/30 overflow-hidden p-4 flex items-center justify-center">
                    <div className="text-center">
                      <meta.icon className="w-10 h-10 mx-auto mb-2 opacity-30" />
                      <p className="text-xs text-text-muted/50 font-medium">{template.style}</p>
                    </div>
                  </div>

                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="text-sm font-semibold text-text-heading line-clamp-1">{template.name}</h3>
                      <div className="flex items-center gap-2 mt-1">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full bg-gradient-to-r ${meta.gradient} text-white/90`}>
                          {template.category}
                        </span>
                        <span className="text-[10px] text-text-muted capitalize">{template.style}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-1 text-xs text-text-muted">
                      <Download className="w-3 h-3" />
                      {template.download_count || 0}
                    </div>
                  </div>

                  <button
                    onClick={(e) => { e.stopPropagation(); handlePreview(template); }}
                    className="w-full mt-3 py-2 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-xs font-semibold btn-luxury flex items-center justify-center gap-1.5 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-2 group-hover:translate-y-0"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    Preview & Use
                  </button>
                </div>
              </motion.div>
            );
          })}
        </div>
      ) : (
        <div className="space-y-2">
          {filtered.map((template, i) => {
            const meta = getCategoryMeta(template.category);
            return (
              <motion.div
                key={template.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.03 }}
                onClick={() => handlePreview(template)}
                className="group relative flex items-center justify-between p-4 rounded-xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all cursor-pointer overflow-hidden"
              >
                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                  <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
                </div>
                <div className="relative flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${meta.gradient} p-2.5 flex items-center justify-center`}>
                    <meta.icon className="w-full h-full text-white" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-text-heading">{template.name}</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-[11px] text-text-muted capitalize">{template.category}</span>
                      <span className="text-[10px] text-text-muted/50">·</span>
                      <span className="text-[11px] text-text-muted capitalize">{template.style}</span>
                    </div>
                  </div>
                </div>
                <div className="relative flex items-center gap-3">
                  <div className="flex items-center gap-1.5 text-xs text-text-muted">
                    <Download className="w-3 h-3" />
                    {template.download_count || 0}
                  </div>
                  <Eye className="w-4 h-4 text-text-muted group-hover:text-primary transition-colors" />
                  <ChevronRight className="w-4 h-4 text-text-muted group-hover:text-primary group-hover:translate-x-0.5 transition-all" />
                </div>
              </motion.div>
            );
          })}
        </div>
      )}

      {/* Preview Modal */}
      <AnimatePresence>
        {selectedTemplate && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/70 backdrop-blur-xl z-50 flex items-center justify-center p-4"
            onClick={() => setSelectedTemplate(null)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="w-full max-w-3xl max-h-[85vh] glass-panel-strong rounded-2xl overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b border-border/40">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 p-2.5 flex items-center justify-center">
                    <FileText className="w-full h-full text-white" />
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-text-heading">{selectedTemplate.name}</h2>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-xs px-2 py-0.5 rounded-full bg-primary/15 text-primary border border-primary/20 capitalize">{selectedTemplate.category}</span>
                      <span className="text-xs text-text-muted capitalize">{selectedTemplate.style} style</span>
                      <span className="text-xs text-text-muted flex items-center gap-1">
                        <Download className="w-3 h-3" />
                        {selectedTemplate.download_count || 0} downloads
                      </span>
                    </div>
                  </div>
                </div>
                <button onClick={() => setSelectedTemplate(null)}
                  className="p-2 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Content */}
              <div className="p-6 overflow-y-auto max-h-[60vh]">
                <pre className="text-sm text-text-heading whitespace-pre-wrap font-sans leading-relaxed bg-surface-light/30 p-4 rounded-xl border border-border/30">
                  {selectedTemplate.content}
                </pre>
              </div>

              {/* Actions */}
              <div className="flex items-center justify-end gap-3 p-6 border-t border-border/40 bg-surface/30">
                <button onClick={() => setSelectedTemplate(null)}
                  className="px-5 py-2.5 rounded-xl text-sm text-text-muted hover:text-text-heading transition-colors border border-border/40">
                  Close
                </button>
                <button
                  className="group relative inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden"
                >
                  <Download className="w-4 h-4" />
                  <span>Use This Template</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Create Modal */}
      <AnimatePresence>
        {showCreateModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowCreateModal(false)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              className="w-full max-w-lg glass-panel-strong rounded-2xl p-6 sm:p-8"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 p-2 flex items-center justify-center">
                    <Plus className="w-full h-full text-white" />
                  </div>
                  <h2 className="text-lg font-semibold text-text-heading">New Template</h2>
                </div>
                <button onClick={() => setShowCreateModal(false)}
                  className="p-2 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <form onSubmit={handleCreate} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Template Name *</label>
                  <input value={createForm.name} onChange={e => setCreateForm({ ...createForm, name: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                    placeholder="e.g., Modern Software Engineer" required />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-text-heading mb-1.5">Category</label>
                    <select value={createForm.category} onChange={e => setCreateForm({ ...createForm, category: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all">
                      <option value="general">General</option>
                      <option value="technical">Technical</option>
                      <option value="creative">Creative</option>
                      <option value="executive">Executive</option>
                      <option value="entry">Entry Level</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-heading mb-1.5">Style</label>
                    <select value={createForm.style} onChange={e => setCreateForm({ ...createForm, style: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all">
                      <option value="modern">Modern</option>
                      <option value="classic">Classic</option>
                      <option value="minimal">Minimal</option>
                      <option value="creative">Creative</option>
                      <option value="professional">Professional</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Content (JSON/HTML template) *</label>
                  <textarea value={createForm.content} onChange={e => setCreateForm({ ...createForm, content: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[200px] resize-y font-mono text-xs"
                    placeholder="Paste your template content here..." required />
                </div>
                <div className="flex justify-end gap-3 pt-2">
                  <button type="button" onClick={() => setShowCreateModal(false)}
                    className="px-5 py-2.5 rounded-xl text-sm text-text-muted hover:text-text-heading transition-colors">Cancel</button>
                  <button type="submit"
                    className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury">Create Template</button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
