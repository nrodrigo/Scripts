package product
import grails.rest.*

@Resource(uri='/item', formats=['json', 'html', 'xml'])
class Item {
    
    String name
    String description
    String manufacturer
    Date receiptDate
    double cost
    double price
    
    static constraints = {
    }
}
