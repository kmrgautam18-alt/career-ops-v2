import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

export type Direction = 'left' | 'right';

export function useNavigationDirection(): Direction {
  const location = useLocation();
  const [direction, setDirection] = useState<Direction>('right');
  const historyRef = useRef<string[]>([]);

  useEffect(() => {
    const path = location.pathname;
    const history = historyRef.current;

    if (history.length === 0) {
      historyRef.current = [path];
      return;
    }

    const lastPath = history[history.length - 1];
    if (lastPath === path) return;

    const prevIndex = history.indexOf(path);
    if (prevIndex !== -1 && prevIndex < history.length - 1) {
      // Already in history → back navigation
      setDirection('left');
      historyRef.current = history.slice(0, prevIndex + 1);
    } else {
      // New path → forward navigation
      setDirection('right');
      historyRef.current = [...history, path];
    }
  }, [location.pathname]);

  return direction;
}
