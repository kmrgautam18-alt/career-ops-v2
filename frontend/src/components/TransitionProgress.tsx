import { motion, AnimatePresence } from 'framer-motion';

interface TransitionProgressProps {
  visible: boolean;
}

export function TransitionProgress({ visible }: TransitionProgressProps) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="absolute top-0 left-0 right-0 z-50 h-[2px] overflow-hidden pointer-events-none"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0, transition: { duration: 0.3 } }}
        >
          {/* Background track */}
          <div className="absolute inset-0 bg-primary/10" />

          {/* Animated bar */}
          <motion.div
            className="absolute inset-y-0 left-0 bg-gradient-to-r from-primary via-accent to-primary"
            initial={{ width: '0%', x: '-100%' }}
            animate={{
              width: ['0%', '70%', '85%'],
              x: ['-100%', '0%', '15%'],
            }}
            transition={{
              duration: 1.2,
              ease: [0.25, 0.46, 0.45, 0.94],
              times: [0, 0.3, 1],
            }}
            style={{ borderRadius: '0 2px 2px 0' }}
          />

          {/* Glow effect */}
          <motion.div
            className="absolute top-0 right-0 w-[60px] h-full bg-gradient-to-r from-transparent to-accent/60 blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0.6] }}
            transition={{
              duration: 1.2,
              ease: 'easeInOut',
              times: [0, 0.4, 1],
            }}
            style={{ transform: 'translateX(100%)' }}
          />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
