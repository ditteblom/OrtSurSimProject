import argparse
from solver import Solver
from dataloader import get_loader
import torchvision.transforms as transforms
from datetime import datetime


def str2bool(v):
    return v.lower() in ('true')

def main(config):
    size = 224

    # data augmentation
    train_transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Resize((size,size)),
                                    transforms.RandomHorizontalFlip(),
                                    #transforms.Grayscale(num_output_channels = 1),
                                    transforms.RandomChoice([transforms.GaussianBlur(kernel_size=3, sigma=(1, 1)),
                                    transforms.RandomRotation(degrees=(15)),])
                                    ])
    val_transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Resize((size,size)),
                                    #transforms.Grayscale(num_output_channels = 1),
                                    ])

    # Data loaders.
    train_loader = get_loader(config.repair_type, 'train', config.data_dir, config.batch_size, transform = train_transform)
    val_loader = get_loader(config.repair_type, 'val', config.data_dir, config.batch_size, transform = val_transform)

    print('Data loaded. Start training...')

    solver = Solver(train_loader, val_loader, config)

    solver.train()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Model configuration.
    parser.add_argument('--repair_type', type=str, default='001_hansson_pin_system', help='type of fracture repair')
    parser.add_argument('--actfun', type=str, default='relu', help='type of activation function')
    parser.add_argument('--alpha', type=float, default='1', help='alpha for elu activation function')
    
    # Training configuration.
    parser.add_argument('--data_dir', type=str, default='Data/')
    parser.add_argument('--batch_size', type=int, default=12, help='batch size')
    parser.add_argument('--num_iters', type=int, default=1000, help='number of total iterations')
    parser.add_argument('--learning_rate', type=float, default=0.00001, help='learning rate for optimizer')
    
    # Miscellaneous.
    parser.add_argument('--log_step', type=int, default=1)
    parser.add_argument('--run_name', type=str, default=datetime.now().strftime('%y%B%d_%H%M_%S'))

    config = parser.parse_args()
    print(config)
    main(config)