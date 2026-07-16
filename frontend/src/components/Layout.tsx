import { useState, useEffect, useRef } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { AnimatePresence, motion, type Variants } from 'framer-motion';
import { Menu } from 'lucide-react';
import { Sidebar } from './Sidebar';
import { PageSkeleton } from './PageSkeleton';
import { DirectionIndicator } from './DirectionIndicator';
import { TransitionProgress } from './TransitionProgress';
import { useNavigationDirection } from '../hooks/useNavigationDirection';
import type { Direction } from '../hooks/useNavigationDirection';

function slideVariants(direction: Direction, isEntering: boolean): Variants {
  const offset = 60;
  const enterFrom = isEntering ? (direction === 'right' ? offset : -offset) : 0;
  const exitTo = direction === 'right' ? -offset : offset;

  return {
    initial: {
      opacity: 0,
      x: enterFrom,
      scale: 0.97,
    },
    animate: {
      opacity: 1,
      x: 0,
      scale: 1,
      transition: {
        duration: 0.35,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
    exit: {
      opacity: 0,
      x: exitTo,
      scale: 0.97,
      transition: {
        duration: 0.2,
        ease: 'easeIn',
      },
    },
  };
}

export function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isNavigating, setIsNavigating] = useState(false);
  const location = useLocation();
  const prevKey = useRef(location.key);
  const direction = useNavigationDirection();

  useEffect(() => {
    if (prevKey.current !== location.key) {
      prevKey.current = location.key;
      setIsNavigating(true);
      const timer = setTimeout(() => setIsNavigating(false), 600);
      return () => clearTimeout(timer);
    }
  }, [location.key]);

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Bar */}
        <header className="flex items-center justify-between px-4 lg:px-6 h-14 border-b border-border/40 bg-background/60 backdrop-blur-xl">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden p-2 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-all"
          >
            <Menu className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-3 ml-auto">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-sm">
              <span className="text-xs font-bold text-white">CO</span>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6 relative">
          {/* Transition progress bar */}
          <TransitionProgress visible={isNavigating} />

          {/* Direction indicator arrow */}
          <DirectionIndicator direction={direction} visible={isNavigating} />

          <AnimatePresence mode="wait">
            {isNavigating ? (
              <motion.div
                key="skeleton"
                variants={slideVariants(direction, true)}
                initial="initial"
                animate="animate"
                exit="exit"
                className="relative"
              >
                <PageSkeleton route={location.pathname} />
              </motion.div>
            ) : (
              <motion.div
                key={location.pathname}
                variants={slideVariants(direction, false)}
                initial="initial"
                animate="animate"
                exit="exit"
                className="relative"
              >
                <Outlet />
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}
