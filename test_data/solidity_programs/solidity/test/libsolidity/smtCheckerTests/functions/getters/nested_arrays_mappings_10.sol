pragma experimental SMTChecker;

contract C {
	mapping (uint => uint[])[] public m;

	constructor() {
		m.push();
		m[0][1].push();
		m[0][1].push();
		m[0][1].push();
		m[0][1][2] = 42;
	}

	function f() public view {
		uint y = this.m(0,1,2);
		assert(y == m[0][1][2]); // should hold
		assert(y == 1); // should fail
	}
}
// ====
// SMTIgnoreCex: yes
// ----
// Warning 6328: (289-303): CHC: Assertion violation happens here.
