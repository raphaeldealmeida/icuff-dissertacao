<?php
class NoMock {

    function let(NoMock $nomock)
    {
        return null;
    }
}

final class MoneySpec extends ObjectBehavior
{
    /**
     * Initialize the calculator
     */
    function let(Calculator $calculator)
    {
        $this->beConstructedWith($calculator);
    }

    private function noArgs()
    {
        return null;
    }

    /**
     * Compares two amounts using Mocked
     */
    public function it_compares_two_amounts(Mocked $mockeds, Mocked2 $mocking)
    {
        return 1 + 1;
    }
}