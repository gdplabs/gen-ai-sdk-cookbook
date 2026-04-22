import { useRef, useEffect, DependencyList } from "react";

export function useAutoScroll(deps: DependencyList) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    ref.current?.scrollIntoView({ behavior: "smooth" });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return ref;
}
