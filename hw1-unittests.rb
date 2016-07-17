require 'unirest'
require "test/unit"
 
class TestSimpleNumber < Test::Unit::TestCase
 
  def test1
    res = Unirest.get('http://localhost:49160/hello')
    assert_equal(res.raw_body, 'Hello world!', 'GET on the hello resource did not execute successfully')
  end

 
  def test2
    res = Unirest.get('http://localhost:49160/echo')
    assert_equal(res.raw_body, '', 'GET echo without a msg should have output a blank.')
  end

 
  def test3
    res = Unirest.get('http://localhost:49160/echo?msg=HolyShitItWorked')
    assert_equal(res.raw_body, 'HolyShitItWorked', 'GET echo with a message did not execute successfully')
  end
    
 
  def test4
    res = Unirest.get('http://localhost:49160/whodidyouthinkyouare')
    assert_equal(res.code, 404, 'GET on random unknown resource should have failed, but did not.')
  end

 
  def test5
    res = Unirest.post('http://localhost:49160/hello')
    assert_not_equal(res.code, 200, 'POST on hello should not have worked, but returned successfully.')
    assert_equal(res.code, 405, 'POST should have returned a 405 METHOD NOT ALLOWED.')
  end

 
  def test6
    res = Unirest.post('http://localhost:49160/echo?msg=somethingintheway')
    assert_not_equal(res.code, 200, 'POST on echo should not have worked, but returned successfully.')
    assert_equal(res.code, 405, 'POST should have returned a 405 METHOD NOT ALLOWED.')
  end
    
 
  def test7
    res = Unirest.get('http://localhost:49160/hello21234')
    assert_not_equal(res.code, '200', 'GET on the hello21234 resource should not execute successfully, but it did')
  end

 
  def test8
    res = Unirest.get('http://localhost:49160/echo?msg=')
    assert_equal(res.raw_body, '', 'GET echo without a msg should have output a blank.')
  end

 
  def test9
    res = Unirest.get('http://localhost:49160/hello?msg=AnyColourYouLike')
    assert_equal(res.raw_body, 'Hello world!', 'GET hello with a message did not execute successfully')
  end
    
 
  def test10
    res = Unirest.get('http://localhost:49160/anyUnknownMethod')
    assert_equal(res.code, 404, 'GET on random unknown resource should have failed, but did not.')

  end
 
end
