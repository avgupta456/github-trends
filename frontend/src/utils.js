export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function classnames(...args) {
  return args.join(' ');
}
