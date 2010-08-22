package jycessing;

import org.python.core.PyInteger;

abstract public class WrappedInteger extends PyInteger {

    abstract public int getValue();

    public WrappedInteger() {
        super(0);
    }

}
