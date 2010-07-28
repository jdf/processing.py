package jycessing;

import java.lang.reflect.Method;

public class Bench {
	long c;

	public long meth(final long arg) {
		return c += arg;
	}

	static long time(final Runnable b, final int iters) {
		final long start = System.currentTimeMillis();
		for (int i = 0; i < iters; i++) {
			b.run();
		}
		return System.currentTimeMillis() - start;
	}

	public static void main(final String[] args) throws Exception {
		final Method meth = Bench.class.getMethod("meth", long.class);
		final Bench bench = new Bench();
		final long directTime = time(new Runnable() {
			@Override
			public void run() {
				bench.meth(System.currentTimeMillis());
			}
		}, 1000000);
		System.out.println(bench.c);
		System.out.println("direct: " + directTime + "ms");
		final long dynamicTime = time(new Runnable() {
			@Override
			public void run() {
				try {
					meth.invoke(bench, System.currentTimeMillis());
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}, 1000000);
		System.out.println(bench.c);
		System.out.println("dynamic: " + dynamicTime + "ms");
	}
}
