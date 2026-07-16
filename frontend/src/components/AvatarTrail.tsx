import { motion, AnimatePresence } from 'framer-motion';

interface AvatarTrailProps {
  fromY: number;
  toY: number;
  visible: boolean;
}

export function AvatarTrail({ fromY, toY, visible }: AvatarTrailProps) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="absolute left-3 right-3 z-40 pointer-events-none"
          initial={false}
          animate={{ y: toY - fromY, opacity: 1 }}
          exit={{ opacity: 0, scale: 0.8, transition: { duration: 0.15 } }}
          transition={{
            y: {
              duration: 0.45,
              ease: [0.25, 0.46, 0.45, 0.94],
            },
          }}
          style={{ y: 0 }}
        >
          {/* Glow layer */}
          <motion.div
            className="absolute inset-0 rounded-xl"
            initial={{ opacity: 0.6 }}
            animate={{
              opacity: [0.6, 1, 0.6],
              boxShadow: [
                '0 0 20px rgba(99,102,241,0.3)',
                '0 0 40px rgba(99,102,241,0.5)',
                '0 0 20px rgba(99,102,241,0.3)',
              ],
            }}
            transition={{ duration: 1.2, repeat: Infinity, ease: 'easeInOut' }}
          />

          {/* Orb content */}
          <div className="relative flex items-center gap-3 px-3.5 py-2.5 rounded-xl bg-gradient-to-r from-primary/20 via-primary/10 to-accent/10 border border-primary/30 shadow-lg shadow-primary-glow/30">
            {/* Inner glow */}
            <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary/10 via-accent/5 to-transparent" />

            {/* Icon */}
            <div className="relative z-10 w-5 h-5 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-sm">
              <div className="w-2 h-2 rounded-full bg-white" />
            </div>

            {/* Label shimmer */}
            <div className="relative z-10 h-3 w-16 rounded-full bg-white/10 overflow-hidden">
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
                animate={{ x: ['-100%', '200%'] }}
                transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
              />
            </div>
          </div>

          {/* Tail trail */}
          <motion.div
            className="absolute right-0 top-1/2 -translate-y-1/2 w-12 h-[2px]"
            initial={{ opacity: 0.6, scaleX: 1 }}
            animate={{
              opacity: [0.6, 0.2, 0.6],
              scaleX: [1, 1.5, 1],
            }}
            transition={{ duration: 1, repeat: Infinity, ease: 'easeInOut' }}
            style={{ transformOrigin: 'left center' }}
          >
            <div className="w-full h-full bg-gradient-to-l from-primary/60 via-accent/30 to-transparent rounded-full" />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
