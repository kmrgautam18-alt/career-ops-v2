import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import type { Direction } from '../hooks/useNavigationDirection';

interface DirectionIndicatorProps {
  direction: Direction;
  visible: boolean;
}

export function DirectionIndicator({ direction, visible }: DirectionIndicatorProps) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          key={direction}
          initial={{ opacity: 0, scale: 0.5, x: direction === 'right' ? -10 : 10 }}
          animate={{ opacity: 1, scale: 1, x: 0 }}
          exit={{ opacity: 0, scale: 0.5, transition: { duration: 0.15 } }}
          transition={{ duration: 0.25, ease: 'easeOut' }}
          className={`
            fixed top-1/2 -translate-y-1/2 z-50
            pointer-events-none
            ${direction === 'right' ? 'left-4 sm:left-8' : 'right-4 sm:right-8'}
          `}
        >
          <motion.div
            initial={{ x: direction === 'right' ? -20 : 20 }}
            animate={{ x: direction === 'right' ? [0, 8, 0] : [0, -8, 0] }}
            transition={{
              duration: 0.8,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
            className="
              w-12 h-12 sm:w-14 sm:h-14
              rounded-2xl
              bg-background/70 backdrop-blur-xl
              border border-border/40
              flex items-center justify-center
              shadow-xl shadow-black/20
            "
          >
            <div className="relative">
              {/* Outer glow */}
              <div className="absolute inset-0 rounded-full bg-gradient-to-br from-primary/30 to-accent/30 blur-xl scale-150" />

              {/* Icon */}
              <div className="relative w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
                {direction === 'right' ? (
                  <ChevronRight className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
                ) : (
                  <ChevronLeft className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
                )}
              </div>
            </div>
          </motion.div>

          {/* Direction label */}
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="text-center mt-2"
          >
            <span className="text-[10px] font-medium text-text-muted/60 uppercase tracking-widest">
              {direction === 'right' ? 'Forward' : 'Back'}
            </span>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
